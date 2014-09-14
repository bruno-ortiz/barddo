from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from notifications.models import Notification


@dajaxice_register
def mark_notifications_as_read(request):
    user = request.user

    Notification.objects.mark_all_as_read(user)

    ajax = Dajax()
    ajax.script("notification_read_callback();")
    return ajax.json()