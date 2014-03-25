# -*- coding: utf-8 -*-
import datetime

from django.db import models

from django.db.models.manager import Manager

from accounts.models import BarddoUser
from core.models import Collection


__author__ = 'jovial'


class RatingManager(Manager):
    def like_count(self, collection):
        return self.filter(collection=collection, like=True).count()


class Rating(models.Model):
    class Meta:
        unique_together = ('user', 'collection')

    user = models.ForeignKey(BarddoUser, null=False)
    collection = models.ForeignKey(Collection, null=False, related_name='like')
    date = models.DateTimeField(null=False)
    like = models.BooleanField(null=False)

    objects = RatingManager()


def user_likes(user, collection):
    try:
        rating = Rating.objects.get(user=user, collection=collection)
        return rating.like
    except Rating.DoesNotExist:
        return False


def add_like(user, collection):
    try:
        rating = Rating.objects.get(user=user, collection=collection)
        rating.like = True
    except Rating.DoesNotExist:
        rating = Rating(user=user, collection=collection,
                        date=datetime.datetime.now(), like=True)
    rating.save()


def remove_like(user, collection):
    Rating.objects.filter(user=user, collection=collection).delete()