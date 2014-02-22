from django.core.validators import MaxLengthValidator
from django.db import models

__author__ = 'jovial'


class Feedback(models.Model):
    name = models.CharField(max_length=30)
    address = models.EmailField()
    feedback = models.TextField(validators=[MaxLengthValidator(500)])
    date = models.DateTimeField()