from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.query import QuerySet
from django.db.models import Q
from polymorphic import PolymorphicModel
from django.contrib.sites.models import Site


class FeedManager(models.Manager):
    def get_queryset(self):
        return FeedQuerySet(self.model, using=self._db)

    def feed_for_user(self, user):
        return self.get_queryset().feed_for_user(user)


class FeedQuerySet(QuerySet):
    def feed_for_user(self, user):
        return self.filter(Q(user=user) | Q(action__object_id=user.id)).select_related("user_profile").order_by(
            "-created")


class FeedAction(PolymorphicModel):
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')


class UserFeed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(default=timezone.now)
    action = models.ForeignKey(FeedAction)

    objects = FeedManager()

    def get_picture(self):
        return self.action.get_picture()

    def get_message(self):
        return self.action.get_message(self.user)

    def get_elapsed(self):
        return self.created


class JoinAction(FeedAction):
    def get_picture(self):
        return '<i class="pull-left thumbicon icon-key btn-info no-hover"></i>'

    def get_message(self, user):
        return _('<b>Barddo</b> welcomes <a class="user" href="{}">{}</a>! Aho! Aho! Aho!').format(user.user_url(), user.first_name)


class CollectionSubscribeAction(FeedAction):
    def get_picture(self):
        return '<i class="pull-left thumbicon icon-key btn-info no-hover"></i>'

    def get_message(self, user):
        return _('<b>Barddo</b> Subscribes <a class="user" href="{}">{}</a>! Aho! Aho! Aho!').format(user.user_url(), user.first_name)


class FollowAction(FeedAction):
    def get_picture(self):
        current_site = Site.objects.get_current()
        return '<img class="pull-left" alt="avatar" src="http://{}{}"/>'.format(current_site, self.target.profile.avatar.url)

    def get_message(self, user):
        return _('<a class="user" href="{}">{}</a> started to follow <a class="user" href="{}">{}</a>.').format(user.user_url(), user.first_name,
                                                                                                                self.target.user_url(), self.target.first_name)


class UnFollowAction(FeedAction):
    def get_picture(self):
        current_site = Site.objects.get_current()
        return '<img class="pull-left" alt="avatar" src="http://{}{}"/>'.format(current_site, self.target.profile.avatar.url)

    def get_message(self, user):
        return _('<a class="user" href="{}">{}</a> stopped to follow <a class="user" href="{}">{}</a>.').format(user.user_url(), user.first_name,
                                                                                                                self.target.user_url(), self.target.first_name)
