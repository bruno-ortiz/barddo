from django.forms import ModelForm, DateField
from barddo_auth.models import BarddoUser, BarddoUserProfile

__author__ = 'bruno'


class BarddoUserForm(ModelForm):
    class Meta:
        model = BarddoUser
        fields = ['username', 'email']


class BarddoUserProfileForm(ModelForm):
    birth_date = DateField(input_formats=('%Y-%m-%dT%H:%M:%S.%fZ',))

    class Meta:
        model = BarddoUserProfile
        field = ['birth_date', 'gender', 'country']
