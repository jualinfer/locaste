from ..models import *
from django.forms import ModelForm, DateInput, Textarea, BooleanField
from django import forms


class QuestionOptionForm(ModelForm):
    class Meta:
        model = QuestionOption
        fields = ['option']
        widgets = {
            'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['desc']
        widgets = {
            'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


class AuthForm(ModelForm):
    # me = BooleanField(initial=True, required=False)

    class Meta:
        model = Auth
        fields = ['name', 'url', 'me']


class VotingForm(ModelForm):
    class Meta:
        model = Voting
        fields = ['name', 'desc', 'gender', 'min_age', 'max_age', 'custom_url', 'public_voting']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
        }