from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from authentication.forms import UserProfileForm, UserForm


from .serializers import UserSerializer

def edit_profile(request):
    template_name="edit_profile.html"
    if request.method == 'POST':
        userProfileForm = UserProfileForm(request.POST, instance=request.user.userprofile)
      
        print(userProfileForm.errors)

        if userProfileForm.is_valid():
            userProfileForm.save()
            return redirect('/authentication/profile')

    else:
        userProfileForm = UserProfileForm(instance=request.user.userprofile)

    args = {'userProfileForm' : userProfileForm}
    return render(request, 'edit_profile.html', args)


class GetUserView(APIView):
    def post(self, request):
        user = None
        if(request.data.get('token')!=None):
            key = request.data.get('token', '')
            tk = get_object_or_404(Token, key=key)
            user = tk.user
        else:
            if request.user.is_authenticated:
                user = request.user
        return Response(UserSerializer(user, many=False).data)

class ProfileView(TemplateView):
    template_name="profile.html"
    def get_context_data(self):
        context=super().get_context_data()
        return context


class LogoutView(TemplateView):
    template_name="logout.html"
    def get_context_data(self):
        context=super().get_context_data()
        return context


class IndexView(TemplateView):
    template_name="index.html"
    def get_context_data(self):
        context=super().get_context_data()
        return context

class SigninView(TemplateView):
    template_name="signin.html"
    def get_context_data(self):
        context=super().get_context_data()
        return context

class SignupView(TemplateView):
    template_name="signup.html"
    def get_context_data(self):
        context=super().get_context_data()
        return context