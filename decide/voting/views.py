import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from django.views import generic
from django.db import connection

from .models import Question, QuestionOption, Voting
from .serializers import VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from .forms.forms import VotingForm, QuestionForm, QuestionOptionForm, AuthForm
from django.db import transaction
import json
import urllib

CAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'

# Error messages
CAPTCHA_ERROR_MESSAGE = 'Invalid CAPTCHA. Please try again.'
CUSTOM_URL_ERROR_MESSAGE = "Custom URL field cannot contain \'/\' or whitespaces."
MAX_AGE_MIN_AGE_ERROR_MESSAGE = "Max age cannot be lower than min age."

voting_form = None
question_forms = []
auth_form = None
auth_forms = []
question_option_forms = []


def check_voting_form_restrictions(form, request):
    correct = True
    error_message = ''

    custom_url = form["custom_url"].value()
    max_age = form["max_age"].value()
    min_age = form["min_age"].value()

    if not captcha_is_correct(request):
        correct = False
        error_message = CAPTCHA_ERROR_MESSAGE
    elif '/' in custom_url or ' ' in custom_url:
        correct = False
        error_message = CUSTOM_URL_ERROR_MESSAGE
    elif max_age != '' and min_age != '' and int(max_age) < int(min_age):
        correct = False
        error_message = MAX_AGE_MIN_AGE_ERROR_MESSAGE

    return form.is_valid() and correct, error_message


def votingForm(request):
    global voting_form
    global auth_form
    global auth_forms
    global question_forms
    global question_option_forms
    print(request.POST)
    if request.method == 'POST' and ('gender' in request.POST.keys()):
        voting_form = VotingForm(request.POST)
        correct, error_message = check_voting_form_restrictions(voting_form, request)
        if correct:
            auth_form = AuthForm()
            return render(request, 'voting/form.html', {'form': auth_form, 'is_auth': True})
        else:
            return render(request, 'voting/form.html', {'error': True, 'error_message': error_message,
                                                        'form': voting_form, 'show_captcha': True and settings.ENABLE_CAPTCHA})
    elif request.method == 'POST' and voting_form is not None and voting_form.is_valid() and (
            'url' in request.POST.keys()):
        for i in range(len(request.POST.getlist('name'))):
            name = request.POST.getlist('name')[i]
            url = request.POST.getlist('url')[i]
            #  me = request.POST.getlist("me")[i]
            auth_form = AuthForm({"name": name, "url": url})
            auth_forms.append(auth_form)

        if valid_objects(auth_forms):
            question_form = QuestionForm()
            question_option_form = QuestionOptionForm()
            return render(request, 'voting/questionForm.html',
                          {'question_form': question_form, 'question_option_form': question_option_form,
                           'voting_url': 'http://127.0.0.1:8000/voting/create/'})
        else:
            auth_forms = []
            return render(request, 'voting/form.html', {'form': auth_form, 'is_auth': True})

    elif request.method == 'POST' and voting_form is not None and voting_form.is_valid() and auth_form is not None and auth_form.is_valid() and (
            'descs[]' in request.POST.keys() or  'questionRange' in request.POST.keys()) :

        save_voting(request)

        return render(request, 'voting/list')

    else:
        if voting_form is None or not voting_form.is_valid():
            voting_form = VotingForm()
            print('Voting')
            return render(request, 'voting/form.html', {'form': voting_form, 'show_captcha': True and settings.ENABLE_CAPTCHA})
        elif auth_form is None or not valid_objects(auth_forms):
            auth_form = AuthForm()
            print('Auth')
            return render(request, 'voting/form.html', {'form': auth_form})
        else:
            question_form = QuestionForm()
            question_option_form = QuestionOptionForm()
            return render(request, 'voting/questionForm.html',
                          {'question_form': question_form, 'question_option_form': question_option_form,
                           'voting_url': 'http://127.0.0.1:8000/voting/create/'}, )


def captcha_is_correct(request):
    ''' Begin reCAPTCHA validation '''

    if settings.ENABLE_CAPTCHA:
        recaptcha_response = request.POST.get('g-recaptcha-response')
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(CAPTCHA_URL, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''
        return result['success']
    else:
        return True



class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id',)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'))
        voting.save()
        voting.question.set([question])
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                             defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)


class VotingList(generic.ListView):
    template_name = 'voting/votingList.html'
    context_object_name = 'voting_list'

    def get_queryset(self):
        """
        Return the list of users of the system.
        """
        return Voting.objects.all()




def valid_objects(objects):
    valid = True

    for obj in objects:
        if not obj.is_valid():
            return False

    return valid


@transaction.non_atomic_requests
def save_voting(request):
    global voting_form
    global auth_form
    global auth_forms
    global question_forms
    global question_option_forms
    create_question_options_formularies(request, question_forms, question_option_forms)
    saved_questions = []
    saved_auths = []

    if valid_objects(question_forms):
        valid = True
        for q in question_option_forms:
            valid = valid_objects(q)
            if not valid:
                break
        if valid:
            for question in question_forms:
                model_question = Question(desc=question["desc"].value(),type=question["type"].value())
                model_question.save()
                saved_questions.append(model_question)

            index = 0
            for options in question_option_forms:
                indexNumber = 1
                for option in options:
                    if saved_questions[index].type == "Normal":
                        question_option = QuestionOption(option=option["option"].value(),
                                                     question=saved_questions[index], number=indexNumber,percentage=None,range=None)
                        question_option.save()
                    elif saved_questions[index].type == "Range":
                        question_option = QuestionOption(range=option["range"].value(),
                                                     question=saved_questions[index], number=indexNumber,percentage=None,option=None)
                        question_option.save()
                    elif saved_questions[index].type == "Percentage":
                        question_option = QuestionOption(percentage=option["percentage"].value(),
                                                         question=saved_questions[index], number=indexNumber, option=None,
                                                         range=None)
                        question_option.save()

                    indexNumber +=1
                index +=1

            for auth in auth_forms:
                model_auth = Auth(name=auth["name"].value(), url=auth["url"].value())
                model_auth.save()
                saved_auths.append(model_auth)

            voting = Voting(name=voting_form["name"].value(), desc=voting_form["desc"].value())
            if voting_form["gender"].value() != '':
                voting.gender = voting_form["gender"].value()
            if voting_form["max_age"].value() != '':
                voting.max_age = voting_form["max_age"].value()
            if voting_form["min_age"].value() != '':
                voting.min_age = voting_form["min_age"].value()
            if voting_form["custom_url"].value() != '':
                voting.custom_url = voting_form["custom_url"].value()
            if voting_form["public_voting"].value() != '':
                voting.public_voting = voting_form["public_voting"].value()
            if voting_form["image_header"].value() != '':
                voting.image_header = voting_form["image_header"].value()
            if voting_form["seats"].value() != '':
                voting.seats = voting_form["seats"].value()
            if voting_form["tally_type"].value() != '':
                voting.seats = voting_form["tally_type"].value()
            voting.save()
            voting.question.set(saved_questions)
            voting.auths.set(saved_auths)
            voting.save()

            voting_form = None
            question_forms = []
            auth_form = None
            auth_forms = []
            question_option_forms = []
            print('voting saved')
    else:
        question_form = QuestionForm()
        question_option_form = QuestionOptionForm()
        question_forms=[]
        question_option_forms = []
        return render(request, 'voting/questionForm.html',
                      {'question_form': question_form, 'question_option_form': question_option_form,
                       'voting_url': 'http://127.0.0.1:8000/voting/create/'})


def create_question_options_formularies(request,question_forms,question_option_forms):
    typesList =[]
    answers = []
    questions = []
    normalQuestionIndex = 0

    #obtenemos las preguntas
    for question in dict(request.POST)['descs[]']:
        questions.append(question)

    #obtenemos los tipos de las preguntas
    for type in dict(request.POST)['types[]']:
        typesList.append(type)
        if type == "Normal" :
            normalQuestionIndex += 1

    #obtenemos la lista de preguntas para cada respuesta normal
    for i in range(0,len(questions)):
        index=0
        if typesList[i] == "Normal":
            answerKey = "answers["+ str(i) + "][]"
            answers.append([])
            for answer in dict(request.POST)[answerKey]:
                answers[index].append(answer)

            index+=1


    #montamos los formularios
    for j in range(0,len(questions)):
        index = 0;
        question_forms.append(QuestionForm({'desc': questions[j],'type':typesList[j]}))

        #añadimos respuestas en funcion al tipo de pregunta
        if typesList[j]=="Normal":
            question_option_forms.append([])
            for answer in answers[index]:
                question_option_forms[j].append(QuestionOptionForm({'option': answer,'number':None,'percentage':None,'range':None}))
        elif typesList[j]=="Range":
            #posible cambio en otra issue para que el rango sea configurable
            question_option_forms.append([])
            question_option_forms[j].append(QuestionOptionForm({'option':None,'number':None,'percentage':None,'range':1}))
            question_option_forms[j].append(QuestionOptionForm({'option': None, 'number': None, 'percentage': None,'range':2}))
            question_option_forms[j].append(QuestionOptionForm({'option': None, 'number': None, 'percentage': None,'range':3}))
            question_option_forms[j].append(QuestionOptionForm({'option': None, 'number': None, 'percentage': None,'range':4}))
            question_option_forms[j].append(QuestionOptionForm({'option': None, 'number': None, 'percentage': None,'range':5}))

        elif typesList[j]=="Percentage":
            percentage = 0
            question_option_forms.append([])
            # posible cambio en otra issue para que el porcentaje sea configurable
            for b in range(0,21):
                question_option_forms[j].append(QuestionOptionForm({'option':None,'number':None,'percentage':percentage/100}))
                percentage += 5
                b+=1

        j+=1




def voting_statistics(request):
    statistics =[
         ['Voting with questions of type normal:'],
         ['Voting with questions of type range:'] ,
         ['Voting with questions of type percentage:'],
         ['Percentage of Voting with questions of type normal:'],
         ['Percentage of Voting with questions of type range:'],
         ['Percentage of Voting with questions of type percentage:'],
         ['Average number of questions per voting:'],
         ['Average number of options per question:'],
         ['Total votings:'],
         ['Total questions:'],
         ['Total options:']
    ]


    #Calculamos los datos
    votingQuestionsNormal = Voting.objects.filter(question__type__contains="Normal").distinct().count()
    votingQuestionsPercentage = Voting.objects.filter(question__type__contains="Range").count()
    votingQuestionsRange = Voting.objects.filter(question__type__contains="Percentage").count()
    num_questions = Question.objects.all().count()
    num_options = QuestionOption.objects.all().count()
    totalVotings = Voting.objects.all().count()

    #Seteamos las variables
    statistics[0].append(votingQuestionsNormal)
    statistics[1].append(votingQuestionsRange )
    statistics[2].append(votingQuestionsPercentage)
    statistics[3].append(votingQuestionsNormal / totalVotings)
    statistics[4].append(votingQuestionsRange / totalVotings)
    statistics[5].append(votingQuestionsPercentage / totalVotings)
    statistics[6].append(num_questions / totalVotings)
    statistics[7].append(num_options / num_questions)
    statistics[8].append(totalVotings)
    statistics[9].append(num_questions)
    statistics[10].append(num_options)





    return render(request,'voting/votingStatistics.html',
                  {'statistics': statistics,
                   'voting_url': 'http://127.0.0.1:8000/voting/statistics/'}, )

