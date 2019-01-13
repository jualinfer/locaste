from ..models import *
from django.forms import ModelForm, DateInput, Textarea, BooleanField
from django import forms


class QuestionOptionForm(ModelForm):
    class Meta:
        model = QuestionOption
        fields = ['option','number','percentage','range']
        widgets = {
            'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['desc', 'type']
        widgets = {
            'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
            'type': forms.widgets.Select(attrs={'readonly': True, 'disabled': True}),
        }


class AuthForm(ModelForm):
    # me = BooleanField(initial=True, required=False)

    class Meta:
        model = Auth
        fields = ['name', 'url', 'me']


class VotingForm(ModelForm):
    class Meta:
        model = Voting
        fields = ['name', 'desc', 'image_header', 'gender', 'min_age', 'max_age', 'custom_url', 'public_voting',
                  'seats', 'tally_type']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'desc': Textarea(attrs={'cols': 80, 'rows': 20}),
        }