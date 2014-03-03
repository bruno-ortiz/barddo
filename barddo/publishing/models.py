from django.db import models

from accounts.models import BarddoUser
from core.models import Collection


__author__ = 'bruno'


class PublishingHouse(models.Model):
    name = models.CharField(max_length=40)
    avatar = models.ImageField(upload_to='publisher_avatar/')
    info = models.TextField()
    collections = models.ForeignKey(Collection)
    publishers = models.ManyToManyField(BarddoUser)