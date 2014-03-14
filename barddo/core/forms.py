from django.forms import ModelForm, DateTimeField, ImageField
from django.conf import settings

from .models import Collection, Work


class CollectionForm(ModelForm):
    """
    Simple collection form that don't expose the user as author. This will be handled at collection creation time.
    """
    start_date = DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Collection
        fields = ['name', 'summary', 'unit', 'start_date']
        exclude = ['author']


class WorkForm(ModelForm):
    """
    Simple work form that don't require the image. That will be validated by an AJAX callback in the application.
    """
    cover = ImageField(required=False)

    class Meta:
        model = Work
        fields = ['title', 'summary', 'unit_count', 'collection', 'cover']
