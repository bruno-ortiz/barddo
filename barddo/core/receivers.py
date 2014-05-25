from django.dispatch import receiver
from redis_metrics import metric

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