from django.dispatch.dispatcher import receiver

from core.models import Work
from notifications.models import WorkLikedNotification
from rating.signals import work_liked


@receiver(work_liked)
def handle_work_liked(sender, **kwargs):
    work_id = kwargs["work_id"]
    work = Work.objects.select_related("author").get(id=work_id)
    WorkLikedNotification.objects.create(actor=sender, action_object=work, recipient=work.author)