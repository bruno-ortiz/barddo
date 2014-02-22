from django import forms

from .models import Feedback


__author__ = 'jose'


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['date']