# -*- coding: utf-8 -*-
import datetime

from django.db import models

from django.db.models.manager import Manager

from accounts.models import BarddoUser
from core.models import Work


__author__ = 'jovial'


class RatingManager(Manager):
    def like_count(self, work):
        return self.filter(work=work, like=True).count()


class Rating(models.Model):
    class Meta:
        unique_together = ('user', 'work')

    user = models.ForeignKey(BarddoUser, null=False)
    work = models.ForeignKey(Work, null=False, related_name='like')
    date = models.DateTimeField(null=False)
    like = models.BooleanField(null=False)

    objects = RatingManager()


def user_likes(user, work):
    rating = Rating.objects.filter(user=user, work=work)
    if rating:
        return rating.like
    else:
        return False


def add_like(user, work):
    rating = Rating.objects.filter(user=user, work=work)
    if rating:
        rating.like = True
    else:
        rating = Rating(user=user, work=work,
                        date=datetime.datetime.now(), like=True)
    rating.save()


def remove_like(user, work):
    rating = Rating.objects.filter(user=user, work=work)
    if rating:
        rating.delete()
