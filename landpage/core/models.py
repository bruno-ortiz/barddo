from django.db import models


class UserContact(models.Model):
    """
    A simple entity to hold user contact messages
    """
    name = models.CharField("Name", max_length=255)
    email = models.EmailField("Email")
    message = models.TextField("Message")