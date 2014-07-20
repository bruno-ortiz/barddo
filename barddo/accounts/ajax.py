from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from accounts.forms import BarddoUserForm, BarddoUserProfileForm
from accounts.models import BarddoUser, BarddoUserProfile
from follow.models import Follow


@login_required
@dajaxice_register
def follow_or_unfollow(request, user_id):
    """
    Toggle given user following on request user
    """
    ajax = Dajax()
    current_user = request.user
    viewing_user = BarddoUser.objects.get(id=user_id)
    follows = Follow.objects.follows(current_user, viewing_user)

    if follows:
        Follow.objects.remove_follower(current_user, viewing_user)
        ajax.script('user_unfollowed_callback()')

    else:
        Follow.objects.add_follower(current_user, viewing_user)
        ajax.script('user_followed_callback()')

    return ajax.json()


@login_required
@dajaxice_register
def edit_profile(request, model, _id, field, value):
    """
    Profile per field editing
    """
    ajax = Dajax()
    form = __get_form_for_model(model, _id, field, value)
    if form.is_valid():
        form.save()
        ajax.remove_css_class('#id_{0}'.format(field), 'field-error')
        ajax.add_css_class('#id_{0}'.format(field), 'field-success')
    else:
        ajax.remove_css_class('#id_{0}'.format(field), 'field-success')
        ajax.add_css_class('#id_{0}'.format(field), 'field-error')
        errors = form.errors[field]
        ajax.script("error_tooltip('#id_%s', '%s');" % (field, "<br />".join(errors)))
    return ajax.json()


def __get_form_for_model(model, _id, field, value):
    """
    Return a specific form object accordingly with model type
    """
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