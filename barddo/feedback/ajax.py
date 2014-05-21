import datetime

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils.translation import ugettext as _

from feedback.forms import FeedbackForm


@dajaxice_register
def send_feedback(request, form_data):
    """
    Register an user feedback
    """
    ajax = Dajax()
    form_data = deserialize_form(form_data)
    form = FeedbackForm(data=form_data)

    for field in form.fields:
        ajax.script('$("#{}").closest("div.form-group").removeClass("has-error")'.format(field))

    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.date = datetime.datetime.now()
        feedback.save()
        ajax.script('callback_feedback_ok("{}", "{}")'.format(_('Success'), _('Feedback sent!')))
    else:
        ajax.script('callback_feedback_error()')
        for field, errors in form.errors.items():
            ajax.script('error_tooltip("#{}", "{}", null, null)'.format(field, errors[0]))
            ajax.script('$("#{}").closest("div.form-group").addClass("has-error")'.format(field))

    # TODO: send an email warning us of what's happening

    return ajax.json()
