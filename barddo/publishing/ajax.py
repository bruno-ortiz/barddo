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
    post_data = request.POST.dict()
    post_data['publishers'] = request.POST.getlist('publishers')
    form = PublishingGroupForm(post_data, request.FILES)

    if form.is_valid():
        publishing_group = form.save(commit=False)
        publishing_group.owner = request.user
        publishing_group.save()
        form.save_m2m()
        ajax.script('call_back_create_group_ok()')
    else:
        for field, errors in form.errors.items():
            ajax.script("callback_create_group_error('#id_{}','{}')".format(field, '<br/>'.join(errors)))

    return ajax.json()


@login_required
@dajaxice_register
def validate_group_name(request, group_name):
    """
    Used to validate when group name is unique
    """
    ajax = Dajax()
    group_name = group_name.lower().strip()
    try:
        if group_name:
            PublishingHouse.objects.get(name__iexact=escape(group_name))
        ajax.script('callback_group_name_is_not_avaliable()')

    except PublishingHouse.DoesNotExist:
        ajax.script('callback_group_name_is_avaliable()')

    return ajax.json()