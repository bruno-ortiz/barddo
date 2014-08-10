# coding=utf-8
from django.db.models.signals import post_delete
from django.dispatch import receiver
from easy_thumbnails.files import get_thumbnailer
from redis_metrics import metric

from core.models import WorkPage
from core.signals import work_read


@receiver(work_read)
def handle_work_read(sender, **kwargs):
    """
    Dispatched everytime a work is read
    """
    work = kwargs.get("work")

    # Work metrics
    metric("works_views", category="Work Metrics")
    metric("work_views_{}".format(work.id), category="Work Metrics")

    # User metrics
    metric("user_{}_works_views".format(sender.id), category="User Metrics")
    metric("user_{}_work_{}_views".format(sender.id, work.id), category="User Metrics")


@receiver(post_delete, sender=WorkPage)
def handle_deleted_page(sender, instance, **kwargs):
    """
        Usado para ajustar os indices das páginas de um trabalho sempre que umá
    """
    thumb = get_thumbnailer(instance.image)
    thumb.delete_thumbnails()