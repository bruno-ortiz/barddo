import datetime
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser
from django.db import models

__author__ = 'bruno'


class BarddoUser(AbstractUser):
    is_publisher = models.BooleanField(default=False)


class BarddoUserAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = BarddoUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except BarddoUser.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return BarddoUser.objects.get(pk=user_id)
        except BarddoUser.DoesNotExist:
            return None


class BarddoUserProfile(models.Model):
    user = models.OneToOneField(BarddoUser, related_name='user_profile')
    avatar = models.ImageField(upload_to='user_avatar/')
    birth_date = models.DateField(default=datetime.date.today())
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), default='M')
