# -*- coding: utf-8 -*-
import datetime

from django.db import models

from accounts.models import BarddoUser

__author__ = 'jovial'


class Rating(models.Model):
    class Meta:
        unique_together = ('user', 'work')

    user = models.ForeignKey(BarddoUser)
    # TODO: Usar GenericForeignKey
    work = models.ForeignKey('core.Work', related_name='like')
    date = models.DateTimeField()
    like = models.BooleanField()


def user_likes(user, work):
    try:
        rating = Rating.objects.get(user=user, work=work)
        return rating.like
    except Rating.DoesNotExist:
        return False


def add_like(user, work):
    try:
        rating = Rating.objects.get(user=user, work=work)
        rating.like = True
    except Rating.DoesNotExist:
        rating = Rating(user=user, work=work,
                        date=datetime.datetime.now(), like=True)
    rating.save()


def remove_like(user, work):
    Rating.objects.filter(user=user, work=work).delete()