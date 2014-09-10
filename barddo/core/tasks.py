from celery.app import shared_task
from django.utils.translation import ugettext_noop as _noop
from notifications import notify

from follow.models import Follow


@shared_task
def notify_collection_updated(owner, work):
    collection = work.collection
    subscribers = Follow.objects.followers(collection)
    if owner in subscribers:
        subscribers.remove(owner)
    for subscriber in subscribers:
        notify.send(owner, recipient=subscriber, verb=_noop('published'), action_object=work, target=collection)