import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext as _
from polymorphic.manager import PolymorphicManager
from polymorphic.polymorphic_model import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

if getattr(settings, 'USE_TZ'):
    from django.utils import timezone

    now = timezone.now
else:
    now = datetime.datetime.now


class NotificationQuerySet(PolymorphicQuerySet):
    def unread(self):
        """Return only unread items in the current queryset"""
        return self.filter(unread=True)

    def read(self):
        """Return only read items in the current queryset"""
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient, only_unread=True):
        """Mark as read any unread messages in the current queryset.
        
        Optionally, filter these by recipient first.
        """
        qs = self.unread().filter(recipient=recipient, unread=only_unread)
        qs.update(unread=False)


class NotificationManager(PolymorphicManager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def read(self):
        return self.get_queryset().read()

    def unread(self):
        return self.get_queryset().unread()

    def mark_all_as_read(self, recipient):
        self.get_queryset().mark_all_as_read(recipient)


class Notification(PolymorphicModel):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False)

    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor')
    actor_object_id = models.CharField(max_length=255)
    actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')

    target_content_type = models.ForeignKey(ContentType, related_name='notify_target', blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType, related_name='notify_action_object', blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object = generic.GenericForeignKey('action_object_content_type', 'action_object_object_id')

    timestamp = models.DateTimeField(default=now)

    objects = NotificationManager()

    class Meta:
        ordering = ('-timestamp', )

    def timesince(self, _now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_

        return timesince_(self.timestamp, _now)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

    def picture(self):
        return NotImplementedError()

    def message(self):
        return NotImplementedError()

    def redirect_url(self):
        return '#'


class WorkPublishedNotification(Notification):
    def message(self):
        return _("%(author)s published %(work)s on %(collection)s") % {'author': self.actor.first_name,
                                                                       'work': self.action_object.title,
                                                                       'collection': self.target.name}

    def picture(self):
        return self.action_object.cover

    def redirect_url(self):
        return self.target.get_absolute_url()


class WorkLikedNotification(Notification):
    def message(self):
        return _("%(user)s likes %(work)s!") % {'user': self.actor.first_name, 'work': self.action_object.title}

    def picture(self):
        return self.actor.profile.avatar

    def redirect_url(self):
        return self.actor.user_url()