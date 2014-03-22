# -*- coding: utf-8 -*-
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils.html import escape
from dajaxice.utils import deserialize_form
from django.contrib.auth.decorators import login_required
from pilkit.processors import Crop
from PIL import Image

from core.models import Collection
from .forms import CollectionForm, WorkForm


@login_required
@dajaxice_register
def validate_unique_collection(request, collection_name):
    """
    Used to validate when collection name is unique
    """
    ajax = Dajax()

    try:
        Collection.objects.get(name__iexact=escape(collection_name.lower().strip()))
        ajax.script("callback_collection_name_is_not_avaliable()")

    except Collection.DoesNotExist:
        ajax.script("callback_collection_name_is_avaliable()")

    return ajax.json()


@login_required
@dajaxice_register
def register_a_collection(request, form):
    """
    Called asynchronously to validate/save a new collection.
    Right now we only do a simple model validation.
    """
    ajax = Dajax()
    form = CollectionForm(deserialize_form(form))

    if form.is_valid():
        collection = form.save(commit=False)
        collection.author = request.user
        collection.save()

        ajax.script('callback_validate_collection_ok()')
    else:
        ajax.script('callback_validate_collection_error()')
        ajax.remove_css_class("#collection-form div.form-group", "has-error")

        for field, errors in form.errors.items():
            ajax.script("error_tooltip('#collection-form #id_%s', '%s');" % (field, "<br />".join(errors)))
            ajax.script('$("#collection-form #id_%s").closest("div.form-group").addClass("has-error")' % field)

    return ajax.json()


@login_required
@dajaxice_register
def validate_work_information(request, form):
    """
    Partially validates a new artist work. Basically, we ignore cover validation, that will only be
    considered on a later step
    """
    ajax = Dajax()
    form = WorkForm(deserialize_form(form))

    if not form.is_valid():
        ajax.script('callback_validate_work_error()')
        ajax.remove_css_class("#work-form div.form-group", "has-error")

        for field, errors in form.errors.items():
            print field, errors
            ajax.script("error_tooltip('#id_%s', '%s');" % (field, "<br />".join(errors)))
            ajax.script('$("#work-form #id_%s").closest("div.form-group").addClass("has-error")' % field)
    else:
        ajax.script('callback_validate_work_ok()')

    return ajax.json()


@login_required
@dajaxice_register
def register_a_work(request):
    """
    Create a new artist work. The most important part here, is the cover parsing. We need to save the cover before
    cropping it.

    Note that we also set the collection cover to the new one.
    """
    ajax = Dajax()
    form = WorkForm(request.POST, request.FILES)

    # TODO: validate minimal image size
    if form.is_valid():
        new_work = form.save(commit=False)
        new_work.total_pages = 0
        new_work.save()

        crop_image(new_work, -int(request.POST["crop_x"]), -int(request.POST["crop_y"]),
                   int(request.POST["crop_w"]), int(request.POST["crop_h"]))

        # TODO: only set as collection cover when user opted for it
        new_work.collection.cover = new_work.cover
        new_work.collection.save()

        ajax.script('callback_create_work_ok(' + str(new_work.id) + ')')
    else:
        ajax.script('callback_create_work_error()')
        for field, errors in form.errors.items():
            print field, errors

    return ajax.json()


def crop_image(work, x, y, width, height):
    """
    Crop given image with given coords and size
    """
    image = Image.open(work.cover.path)
    crop = Crop(width=width, height=height, x=x, y=y)
    crop.process(image).save(work.cover.path, 'JPEG', quality=75)