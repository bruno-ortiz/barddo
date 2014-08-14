import datetime

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.generic import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import ugettext as _
from django.conf import settings

from search.search_manager import SearchManager
from follow.models import Follow


class BarddoUserAuthBackend(ModelBackend):
    """
    Default authentication backend. Used when user is registered with username/password.
    # TODO: is this really needed? Will wee really enable this mode in future?
    """

    def authenticate(self, username=None, password=None, **kwargs):
        """
        Matches username and password
        """
        try:
            user = BarddoUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except BarddoUser.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        """
        Return user object for given id
        """
        try:
            return BarddoUser.objects.get(pk=user_id)
        except BarddoUser.DoesNotExist:
            return None


class BarddoUserManager(UserManager):
    """
    Barddo User custom query manager, creates shortcuts for complex queries
    """

    def get_queryset(self):
        """
        Return custom queryset
        """
        return UserQuerySet(self.model, using=self._db)

    def username_startswith(self, name_prefix):
        """
        Filters users that username starts with given name_prefix
        """
        return self.get_queryset().username_startswith(name_prefix)

    def differs_from(self, user_id):
        """
        Get every user that's not the given one
        """
        return self.get_queryset().differs_from(user_id)


class UserQuerySet(QuerySet):
    """
    Custom user database queries
    """

    def username_startswith(self, param):
        return self.filter(username__istartswith=param)

    def differs_from(self, user_id):
        return self.filter(~Q(id=user_id))


class BarddoUser(AbstractUser):
    """
    Model object for a system user that can be an artist or just a reader
    """
    BARDDO_PUBLISHING_GROUP_ID = 1

    user_followee = GenericRelation(Follow, related_name='user_followee', db_index=True)

    objects = BarddoUserManager()

    search_manager = SearchManager()

    def is_publisher(self):
        """
        A publisher is an artist that joined (or created) a publishing group
        """
        owned_publishers = self.publishing_group_owner.all().count()
        num_publishers = self.publishing_group.all().count()
        return (owned_publishers + num_publishers) > 0

    def is_barddo_publisher(self):
        """
        Determine if the artist is joined the barddo publishing group
        """
        return self.publishing_group.filter(pk=self.BARDDO_PUBLISHING_GROUP_ID).count() > 0

    def user_url(self):
        """
        Current user profile complete URL
        """
        return reverse('account.profile', args=(self.id,))

    class Meta:
        index_together = [["username", "first_name", "last_name"], ]


class BarddoUserProfile(models.Model):
    """
    Custom user data
    """
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = ((GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'))

    user = models.OneToOneField(BarddoUser, related_name='profile', db_index=True)
    avatar = models.ImageField(upload_to='user_avatar/')
    birth_date = models.DateField(default=datetime.date.today())
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    country = models.CharField(max_length=30, default=_('Brazil'))


class BankAccount(models.Model):
    user = models.OneToOneField(BarddoUser)
    favored_name = models.CharField(_('Favoured Name'), max_length=100, db_index=True)
    cpf = models.CharField(_('Social Security'), max_length=15, db_index=True)
    bank_code = models.CharField(_('Bank Code'), max_length=5)
    agency = models.CharField(_('Agency'), max_length=8)
    account = models.CharField(_('Bank Account'), max_length=10)