from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import GetUserView, LogoutView, SigninView, SignupView, ProfileView


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('signup/',include('rest_auth.registration.urls')),
    path('sign-up/', SignupView.as_view(), name="signUp"),
    path('sign-in/', SigninView.as_view(), name="signIn"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile")
]
