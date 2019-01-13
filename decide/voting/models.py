from django.db import models
from django.contrib.postgres.fields import JSONField
import json
import os
from base import mods
from base.models import Auth, Key


GENRES_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]

QUESTIONS_TYPES = [
    ("Range", "Range"),
    ("Percentage", "Percentage"),
    ("Normal", "Normal"),
]

TALLY_TYPES = [
    ("SAINTELAGUE", "SAINTELAGUE"),
    ("DHONDT", "DHONDT"),
    ("MAJORREST", "MAJORREST"),
    ("SAINTELAGUEMOD", "SAINTELAGUEMOD"),
]


class Question(models.Model):
    desc = models.TextField()
    type = models.TextField(blank=True, null=True, default=("Normal", "Normal"), choices=QUESTIONS_TYPES)

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    range = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField(blank=True, null=True)
    percentage = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=3)

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        if self.number != None:
            return '{} ({})'.format(self.number, self.number)
        elif self.range != None:
            return '{} ({})'.format(self.range, self.number)
        else :
            return '{} ({})'.format(self.option, self.number)






class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    image_header = models.CharField(max_length=200,blank=True, null=True)
    question = models.ManyToManyField(Question, related_name='voting_questions')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True, choices=GENRES_CHOICES)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    seats = models.IntegerField(blank=True, null=True)
    tally_type = models.TextField(blank=True, null=True, choices=TALLY_TYPES)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    custom_url = models.CharField(max_length=100, blank=True)
    public_voting = models.BooleanField(default=False)

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def get_voters(self, token=''):
        # getting the len of the census of the current voting
        census = mods.get('census', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        return len(census['voters'])

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass
        self.tally = response.json()
        self.save()
        census = self.get_voters(token)

        return self.do_postproc(census)

    def do_postproc(self, census):
        tally = self.tally
        options = []
        for q in self.question.all():
            options.extend(q.options.all())

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = {'type': self.tally_type, 'options': opts, 'census': census}
        print(data)
        directory = "voting/tallies/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = 'tally_voting'+str(self.id)
        with open(directory+file_name+'.json', 'w') as outfile:
            json.dump(data, outfile)

        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

        return directory+file_name+'.json'

    def __str__(self):
        return self.name
