from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Feedback form
    """

    class Meta:
        model = Feedback
        exclude = ['date']