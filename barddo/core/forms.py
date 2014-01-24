from django.forms import ModelForm, DateTimeField, FileField
from .models import Collection


class CollectionForm(ModelForm):

    # TODO: change date format to the settings
    start_date = DateTimeField(input_formats=('%d-%m-%Y',))

    class Meta:
        model = Collection
        fields = ['name', 'summary', 'unit', 'start_date']