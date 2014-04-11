from django.forms import ModelForm, DateTimeField, ImageField, ModelChoiceField
from django.conf import settings
from django.utils.html import escape

from .models import Collection, Work, CollectionUnit


class CollectionForm(ModelForm):
    """
    Simple collection form that don't expose the user as author. This will be handled at collection creation time.
    """
    start_date = DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    unit = ModelChoiceField(queryset=CollectionUnit.objects.all(), empty_label=None, initial=None)

    class Meta:
        model = Collection
        fields = ['name', 'summary', 'unit', 'start_date']
        exclude = ['author']


class WorkForm(ModelForm):
    """
    Simple work form that don't require the image. That will be validated by an AJAX callback in the application.
    """
    publish_date = DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    cover = ImageField(required=False)

    def clean(self):
        cleaned_data = super(WorkForm, self).clean()
        collection = cleaned_data.get("collection")
        unit_count = cleaned_data.get("unit_count")

        if self.instance.pk is None:  # parsing existing work will allow unit conflict
            try:
                Work.objects.get(collection_id=collection.id, unit_count=unit_count)
                # TODO: Change this to a proper validation to a specific field on django 1.7
                self._errors["unit_count"] = [escape("Already exists"), ]
            except Work.DoesNotExist:
                pass

        return cleaned_data

    class Meta:
        model = Work
        fields = ['title', 'summary', 'unit_count', 'collection', 'cover', 'publish_date']
