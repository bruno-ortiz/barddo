# -*- coding: utf-8 -*-
from dajax.core import Dajax
from dajaxice.utils import deserialize_form
from dajaxice.decorators import dajaxice_register

from .forms import UserContactForm


@dajaxice_register
def register_a_collection(request, form):
    """
    Called asynchronously to register a user feecback
    """
    ajax = Dajax()
    form = UserContactForm(deserialize_form(form))

    if form.is_valid():
        form.save()
        ajax.script('callback_feedback_sent()')
    else:
        ajax.script('callback_feedback_error()')
        ajax.remove_css_class("#feedback-form div.form-group", "has-error")

        for field, errors in form.errors.items():
            ajax.script("error_tooltip('#id_%s', '%s');" % (field, "<br />".join(errors)))
            ajax.script('$("#id_%s").closest("div.form-group").addClass("has-error")' % field)

    return ajax.json()