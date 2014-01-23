# -*- coding: utf-8 -*-
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from core.models import Collection
from .forms import CollectionForm
from django.utils.html import escape
from dajaxice.utils import deserialize_form
from django.contrib.auth.decorators import login_required

#@login_required
@dajaxice_register
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


#@login_required
@dajaxice_register
def register_a_collection(request, form):
    ajax = Dajax()
    form = CollectionForm(deserialize_form(form))

    if form.is_valid():
        ajax.script('callback_validate_collection_ok()')
    else:
        ajax.script('callback_validate_collection_error()')
        ajax.remove_css_class("#collection-form div.form-group", "has-error")

        for error in form.errors:
            print error
            ajax.script('$("#id_%s").closest("div.form-group").addClass("has-error")' % error)

    return ajax.json()