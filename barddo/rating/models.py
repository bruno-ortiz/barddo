# -*- coding: utf-8 -*-
import datetime

from django.db import models

from accounts.models import BarddoUser
from rating.signals import work_liked


class Rating(models.Model):
    class Meta:
        unique_together = ('user', 'work')

    user = models.ForeignKey(BarddoUser)
    # TODO: Usar GenericForeignKey
    work = models.ForeignKey('core.Work', related_name='like')
    date = models.DateTimeField()
    like = models.BooleanField()


def user_likes(user, work_id):
    try:
        rating = Rating.objects.get(user=user, work_id=work_id)
        return rating.like
    except Rating.DoesNotExist:
        return False


def add_like(user, work_id):
    try:
        rating = Rating.objects.get(user=user, work_id=work_id)
        rating.like = True
    except Rating.DoesNotExist:
        rating = Rating(user=user, work_id=work_id,
                        date=datetime.datetime.now(), like=True)
    rating.save()
    work_liked.send(user, work_id=work_id)


def remove_like(user, work_id):
    Rating.objects.filter(user=user, work_id=work_id).delete()