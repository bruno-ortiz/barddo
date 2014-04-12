from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserContact(models.Model):
    """
    A simple entity to hold user contact messages
    """
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("Email"))
    message = models.TextField(_("Message"))