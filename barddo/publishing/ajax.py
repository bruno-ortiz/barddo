from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

from publishing.forms import PublishingGroupForm
from publishing.models import PublishingHouse


__author__ = 'bruno'


@login_required
@dajaxice_register
def register_publishing_group(request):
    ajax = Dajax()
    form = PublishingGroupForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        ajax.script('')
    else:
        ajax.script('callback_create_work_error()')
        for field, errors in form.errors.items():
            print field, errors

    return ajax.json()


@login_required
@dajaxice_register
def validate_group_name(request, group_name):
    """
    Used to validate when group name is unique
    """
    ajax = Dajax()
    try:
        PublishingHouse.objects.get(name__iexact=escape(group_name.lower().strip()))
        ajax.script("callback_group_name_is_not_avaliable()")

    except PublishingHouse.DoesNotExist:
        ajax.script("callback_group_name_is_avaliable()")

    return ajax.json()