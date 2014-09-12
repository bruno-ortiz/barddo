from celery.app import shared_task

from follow.models import Follow
from notifications.models import WorkPublishedNotification


@shared_task
def notify_collection_updated(owner, work):
    collection = work.collection
    subscribers = Follow.objects.followers(collection)
    if owner in subscribers:
        subscribers.remove(owner)
    for subscriber in subscribers:
        WorkPublishedNotification.objects.create(actor=owner, recipient=subscriber, action_object=work, target=collection)