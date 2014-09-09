from celery.app import shared_task
from django.utils.translation import ugettext as _
from notifications import notify

from follow.models import Follow


@shared_task
def notify_collection_updated(owner, work):
    collection = work.collection
    subscribers = Follow.objects.followers(collection)
    for subscriber in subscribers:
        notify.send(owner, recipient=subscriber, verb=_('published'), action_object=work, target=collection)