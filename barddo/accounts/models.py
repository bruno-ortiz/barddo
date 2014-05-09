import datetime

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.generic import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import ugettext as _

from search.search_manager import SearchManager

from follow.models import Follow


__author__ = 'bruno'


class BarddoUserManager(UserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def username_startswith(self, param):
        return self.get_queryset().username_startswith(param)

    def differs_from(self, user_id):
        return self.get_queryset().differs_from(user_id)


class UserQuerySet(QuerySet):
    def username_startswith(self, param):
        return self.filter(username__istartswith=param)

    def differs_from(self, user_id):
        return self.filter(~Q(id=user_id))


class BarddoUser(AbstractUser):
    user_followee = GenericRelation(Follow, related_name='user_followee')

    objects = BarddoUserManager()

    search_manager = SearchManager()

    def is_publisher(self):
        owned_publishers = self.publishing_group_owner.all().count()
        num_publishers = self.publishing_group.all().count()
        return (owned_publishers + num_publishers) > 0

    def is_barddo_publisher(self):
        return self.publishing_group.filter(pk=1).count() > 0

    def user_url(self):
        return reverse('account.profile', args=(self.id,))

    class Meta:
        index_together = [["username", "first_name", "last_name"], ]


class BarddoUserAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = BarddoUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except BarddoUser.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return BarddoUser.objects.get(pk=user_id)
        except BarddoUser.DoesNotExist:
            return None


class BarddoUserProfile(models.Model):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = ((GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'))

    user = models.OneToOneField(BarddoUser, related_name='user_profile')
    avatar = models.ImageField(upload_to='user_avatar/')
    birth_date = models.DateField(default=datetime.date.today())
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)
    country = models.CharField(max_length=30, default=_('Brazil'))