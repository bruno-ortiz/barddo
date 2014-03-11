from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required

from publishing.forms import PublishingGroupForm


__author__ = 'bruno'


@login_required
@dajaxice_register
def register_publishing_group(request):
    ajax = Dajax()
    form = PublishingGroupForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()

        ajax.script('callback_create_work_ok()')
    else:
        ajax.script('callback_create_work_error()')
        for field, errors in form.errors.items():
            print field, errors

    return ajax.json()
