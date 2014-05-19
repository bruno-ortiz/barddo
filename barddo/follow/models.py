from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models, IntegrityError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from signals import start_follow, stop_follow
from .exceptions import AlreadyExistsError


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

CACHE_TYPES = {
    'followers': 'fo-{}',
    'following': 'fl-{}-{}',
}

BUST_CACHES = {
    'followers': ['followers'],
    'following': ['following'],
}


def cache_key(cache_type, user_pk, model_name=None):
    """
    Build the cache key for a particular type of cached value
    """
    if model_name:
        return CACHE_TYPES[cache_type].format(user_pk, model_name)
    return CACHE_TYPES[cache_type].format(user_pk)


def bust_cache(cache_type, user_pk, model_class=None):
    """
    Bust our cache for a given type, can bust multiple caches
    """
    bust_keys = BUST_CACHES[cache_type]
    if model_class:
        keys = [CACHE_TYPES[k].format(user_pk, model_class) for k in bust_keys]
    else:
        keys = [CACHE_TYPES[k].format(user_pk) for k in bust_keys]
    cache.delete_many(keys)


class FollowingManager(models.Manager):
    """
    Following manager
    """

    def followers(self, obj):
        """ Return a list of all followers """
        key = cache_key('followers', obj.pk)
        followers = cache.get(key)

        if followers is None:
            qs = Follow.objects.select_related('follower').filter(object_id=obj.pk)
            followers = [u.follower for u in qs]
            cache.set(key, followers)

        return followers

    def following(self, user, followee_class):
        """
        Return a list of all objects of the followee_class the given user follows
        """
        key = cache_key('following', user.pk, followee_class.__name__)
        following = cache.get(key)

        if following is None:
            followee_classname = followee_class.__name__.lower()
            following_ids = Follow.objects.filter(follower=user, content_type__model=followee_classname).values_list('object_id', flat=True)
            following = followee_class.objects.select_related().filter(id__in=following_ids)
            cache.set(key, following)

        return following

    def add_follower(self, follower, followee):
        """
        Create 'follower' follows 'followee' relationship
        """
        if follower == followee:
            raise ValidationError("Users cannot follow themselves")
        relation = Follow(follower=follower, followee=followee)
        try:
            relation.save()
            bust_cache('followers', followee.pk)
            bust_cache('following', follower.pk, followee.__class__.__name__)
        except IntegrityError as e:
            raise AlreadyExistsError("User '{}' already follows '{}'".format((follower, followee)), e)

        start_follow.send(self, follower=follower, followed=followee)

        return relation

    def remove_follower(self, follower, followee):
        """
        Remove 'follower' follows 'followee' relationship
        """
        try:
            content_type = ContentType.objects.get_for_model(followee.__class__)
            rel = Follow.objects.get(follower=follower, content_type=content_type, object_id=followee.pk)
            rel.delete()
            bust_cache('followers', followee.pk)
            bust_cache('following', follower.pk, followee.__class__.__name__)

            stop_follow.send(self, follower=follower, unfollowed=followee)

            return True
        except Follow.DoesNotExist:
            return False

    def follows(self, follower, followee):
        """
        Does follower follow followee? Smartly uses caches if exists
        """
        followers = cache.get(cache_key('following', follower.pk, followee.__class__.__name__))
        following = cache.get(cache_key('followers', followee.pk))

        if followers and followee in followers:
            return True
        elif following and follower in following:
            return True
        else:
            try:
                content_type = ContentType.objects.get_for_model(followee.__class__)
                Follow.objects.get(follower=follower, content_type=content_type, object_id=followee.pk)
                return True
            except Follow.DoesNotExist:
                return False


class Follow(models.Model):
    """
    Model to represent Following relationships
    """
    follower = models.ForeignKey(AUTH_USER_MODEL, related_name='user_following')
    created = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    followee = GenericForeignKey('content_type', 'object_id')

    objects = FollowingManager()

    class Meta:
        verbose_name = _('Following Relationship')
        verbose_name_plural = _('Following Relationships')
        unique_together = ('follower', 'content_type', 'object_id')

    def __unicode__(self):
        return "User #{} follows #{}".format(self.follower_id, self.object_id)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.follower == self.content_type:
            raise ValidationError("Users cannot follow themselves.")
        super(Follow, self).save(*args, **kwargs)