# -*- coding: utf-8 -*-
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from core.models import Collection
from .forms import CollectionForm
from django.utils.html import escape
from dajaxice.utils import deserialize_form
from django.contrib.auth.decorators import login_required

@dajaxice_register
#@login_required
def validate_unique_collection(request, collection_name):
    """
    Used to validate when collection name is valid or not
    """
    ajax = Dajax()

    try:
        Collection.objects.get(name__iexact=escape(collection_name.lower().strip()))
        ajax.script("callback_collection_name_is_not_avaliable()")

    except Collection.DoesNotExist:
        ajax.script("callback_collection_name_is_avaliable()")

    return ajax.json()


@dajaxice_register
def register_a_collection(request, form):
    ajax = Dajax()
    form = CollectionForm(deserialize_form(form))

    if form.is_valid():
        ajax.script('callback_validate_collection_ok()')
    else:
        ajax.script('callback_validate_collection_error()')
        ajax.remove_css_class('#collection-form', 'has-error')
        for error in form.errors:
            print error
            ajax.add_css_class('#id_%s' % error, 'has-error')

    return ajax.json()