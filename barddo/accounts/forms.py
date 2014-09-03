from django.forms import ModelForm, DateField

from accounts.models import BarddoUser, BarddoUserProfile


class BarddoUserForm(ModelForm):
    """
    Simple BarddoUser form to be used on profile page
    """

    class Meta:
        model = BarddoUser
        fields = ['username', 'email']


class BarddoUserProfileForm(ModelForm):
    """
    Simple Profile form to be used on profile page
    """
    # TODO: use settings date format?
    birth_date = DateField(input_formats=('%Y-%m-%dT%H:%M:%S.%fZ',))

    class Meta:
        model = BarddoUserProfile
        field = ['birth_date', 'gender', 'country', 'language']