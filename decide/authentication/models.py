from django.db import models
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    birthdate = models.DateTimeField()
    captcha = ReCaptchaField()
