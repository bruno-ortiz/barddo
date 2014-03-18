from django.forms import ModelForm

from publishing.models import PublishingHouse


__author__ = 'bruno'


class PublishingGroupForm(ModelForm):
    class Meta:
        model = PublishingHouse
        exclude = ['collections', 'owner']