import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from django.views import generic

from .models import Question, QuestionOption, Voting
from .serializers import VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from .forms.forms import VotingForm, QuestionForm, QuestionOptionForm, AuthForm

voting_form = None
question_forms = []
auth_form = None
auth_forms = []
question_option_forms = []


def votingForm(request):
    global voting_form
    global auth_form
    global auth_forms
    global question_forms
    global question_option_forms

    if request.method == 'POST' and ('gender' in request.POST.keys()):
        voting_form = VotingForm(request.POST)
        if voting_form.is_valid():
            auth_form = AuthForm()
            return render(request, 'voting/form.html', {'form': auth_form, 'is_auth': True})

    elif request.method == 'POST' and voting_form is not None and voting_form.is_valid() and ('url' in request.POST.keys()):
        for i in range(len(request.POST.getlist('name'))):

            name = request.POST.getlist('name')[i]
            url = request.POST.getlist('url')[i]
            #  me = request.POST.getlist("me")[i]
            auth_form = AuthForm({"name": name, "url": url})
            auth_forms.append(auth_form)

        if valid_objects(auth_forms):
            question_form = QuestionForm()
            question_option_form = QuestionOptionForm()
            return render(request, 'voting/questionForm.html', {'question_form': question_form, 'question_option_form': question_option_form, 'voting_url': 'http://127.0.0.1:8000/voting/create/'}, )
        else:
            return render(request, 'voting/form.html', {'form': auth_form, 'is_auth': True})

    elif request.method == 'POST' and voting_form is not None and voting_form.is_valid()  and auth_form is not None and auth_form.is_valid() and ('descs[]' in request.POST.keys()):

        index = 0
        for i, j in request.POST.items():
            if "desc" in i:
                for desc in request.POST.getlist(i):
                    question_forms.append(QuestionForm({'desc': desc}))
            elif "answers" in i:
                for option in request.POST.getlist(i):
                    question_option_forms.append([])
                    question_option_forms[index].append(QuestionOptionForm({'option': option}))
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
                    model_question = Question(desc=question["desc"].value())
                    model_question.save()
                    saved_questions.append(model_question)
                for i, question_options in enumerate(question_option_forms):
                    for j, question_option in enumerate(question_options):
                        question_option = QuestionOption(option=question_option["option"].value(),question=saved_questions[i], number=j)
                        question_option.save()
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
            return render(request, 'voting/questionForm.html',
                          {'question_form': question_form, 'question_option_form': question_option_form,
                           'voting_url': 'http://127.0.0.1:8000/voting/create/'})

        return render(request, 'voting/form.html')
    else:
        if voting_form is None or not voting_form.is_valid():
            voting_form = VotingForm()
            print('Voting')
            return render(request, 'voting/form.html', {'form': voting_form})
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


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id', )

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
