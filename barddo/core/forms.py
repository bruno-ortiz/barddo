from django.forms import ModelForm, DateTimeField, ImageField
from .models import Collection, Work


class CollectionForm(ModelForm):

    # TODO: change date format to the settings
    start_date = DateTimeField(input_formats=('%d-%m-%Y',))

    class Meta:
        model = Collection
        fields = ['name', 'summary', 'unit', 'start_date']
        exclude = ['author']


class WorkForm(ModelForm):
    cover = ImageField(required=False)

    class Meta:
        model = Work
        fields = ['title', 'summary', 'unit_count', 'collection', 'cover']
