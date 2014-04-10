from django.db import models

__author__ = 'jovial'


# TODO: use model data to render the form
class Feedback(models.Model):
    name = models.CharField(max_length=30)
    address = models.EmailField()
    feedback = models.TextField(max_length=500)
    date = models.DateTimeField()