from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from barddo_auth.forms import BarddoUserForm, BarddoUserProfileForm
from barddo_auth.models import BarddoUser, BarddoUserProfile


__author__ = 'bruno'


@login_required
@dajaxice_register
def edit_profile(request, model, _id, field, value):
    # value = normalize_value(field, value)
    dajax = Dajax()
    form = get_form(model, _id, field, value)
    if form.is_valid():
        form.save()
        dajax.remove_css_class('#id_{0}'.format(field), 'field-error')
        dajax.add_css_class('#id_{0}'.format(field), 'field-success')
    else:
        dajax.remove_css_class('#id_{0}'.format(field), 'field-success')
        dajax.add_css_class('#id_{0}'.format(field), 'field-error')
        errors = form.errors[field]
        dajax.script("error_tooltip('#id_%s', '%s');" % (field, "<br />".join(errors)))
    return dajax.json()


def get_form(model, _id, field, value):
    if model == 'BarddoUser':
        instance = BarddoUser.objects.get(id=_id)
        data = model_to_dict(instance)
        data[field] = value
        return BarddoUserForm(instance=instance,
                              data=data)
    elif model == 'BarddoUserProfile':
        instance = BarddoUserProfile.objects.get(id=_id)
        data = model_to_dict(instance)
        data[field] = value
        return BarddoUserProfileForm(instance=instance,
                                     data=data)