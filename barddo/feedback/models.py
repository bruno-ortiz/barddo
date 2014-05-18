from django.db import models
from django.utils.translation import ugettext_lazy as _


class Feedback(models.Model):
    """
    A user persisted feedback
    """
    name = models.CharField(_("Name"), max_length=30)
    email = models.EmailField(_("Email"))
    feedback = models.TextField(_("Your Feedback"), max_length=500)
    date = models.DateTimeField(_("Contact Date"))