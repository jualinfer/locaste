from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from voting.models import Voting
from datetime import date


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

    @classmethod
    def create(cls, voting_id, voter_id):

        # check if the user satisfies the voting restrictions
        voter = User.objects.get(id=voter_id)
        voting = Voting.objects.get(id=voting_id)

        if voting.gender and voter.userprofile.gender != voting.gender:
            raise ValidationError('This voting is restricted for a specific Gender')

        birthdate = voter.userprofile.birthdate

        age = None
        if birthdate:
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if voting.min_age and age and age < voting.min_age:
            raise ValidationError("You don't reach the minimum age for this voting")

        if voting.max_age and age and age > voting.max_age:
            raise ValidationError("You exceed the maximum age for this voting")

        census = cls(voting_id=voting_id, voter_id=voter_id)

        return census
