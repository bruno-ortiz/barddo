from django.contrib.contenttypes.generic import GenericRelation
from django.db import models
from django.db.models.fields import CharField

from accounts.models import BarddoUser
from core.models import Collection
from follow.models import Follow


__author__ = 'bruno'


class Country(models.Model):
    country_name = CharField(max_length=50, unique=True)
    country_language = CharField(max_length=50, unique=True)


class PublishingHouse(models.Model):
    name = models.CharField(max_length=40, unique=True)
    avatar = models.ImageField(upload_to='publisher_avatar/')
    info = models.TextField()
    country = models.ForeignKey(Country)
    collections = models.ForeignKey(Collection, blank=True, null=True)
    owner = models.ForeignKey(BarddoUser, related_name='publishing_group_owner')
    publishers = models.ManyToManyField(BarddoUser, blank=True, null=True, related_name='publishing_group')
    followee = GenericRelation(Follow, related_name='publishing_followee')