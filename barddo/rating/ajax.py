from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from rating.models import user_likes, add_like, remove_like

__author__ = 'jovial'


@dajaxice_register
def toggle_rating(request, work): # O que vou receber no work?
    user = request.user
    ajax = Dajax()

    if user.is_authenticated():
        liked = False

        if user_likes(user, work):
            add_like(user, work)
            liked = True
        else:
            remove_like(user, work)

        ajax.script('set_rating("{}", "{}")'.format(work, liked))
    else:
        ajax.script('notify_not_logged()')

    return ajax.json()
