from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from rating.models import user_likes, add_like, remove_like


__author__ = 'jovial'


@dajaxice_register
def toggle_rating(request, work_id):
    user = request.user
    ajax = Dajax()

    if user.is_authenticated():
        liked = False

        if not user_likes(user, work_id):
            add_like(user, work_id)
            liked = True
        else:
            remove_like(user, work_id)

        ajax.script('set_rating({}, {});'.format(work_id, 'true' if liked else 'false'))
    else:
        ajax.script('$("#loginModal").modal("show");')

    return ajax.json()
