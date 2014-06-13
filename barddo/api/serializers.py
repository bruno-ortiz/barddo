from rest_framework.serializers import ModelSerializer, DateTimeField, CharField, SerializerMethodField, IntegerField
from django.contrib.sites.models import Site

from feed.models import UserFeed
from accounts.models import BarddoUser
from core.models import Work


class UserFeedSerializer(ModelSerializer):
    """
    Serializer for a few fields on user feed action
    """
    id = IntegerField(source="id", read_only=True)
    created = DateTimeField(read_only=True)
    picture = CharField(source="get_picture", read_only=True)
    message = CharField(source="get_message", read_only=True)

    class Meta:
        model = UserFeed
        fields = ('id', 'created', 'picture', 'message')


class UserFriendsSerializer(ModelSerializer):
    """
    Serializer for a few fields on user followees
    """
    id = IntegerField(source="id", read_only=True)
    name = CharField(source="get_full_name", read_only=True)
    picture = SerializerMethodField("get_avatar_url")

    def get_avatar_url(self, user):
        """
        Get user avatar with full url
        """
        current_site = Site.objects.get_current()
        return "http://{}{}".format(current_site, user.profile.avatar.url)

    class Meta:
        model = BarddoUser
        fields = ('id', 'name', 'picture')


class SimpleWorkSerializer(ModelSerializer):
    """
    Serializer for a few fields on user favorite works, user for work list
    """
    id = IntegerField(source="id", read_only=True)
    title = CharField(source="title", read_only=True)
    author = CharField(source="author.get_full_name", read_only=True)
    cover = SerializerMethodField("get_cover_url")

    def get_cover_url(self, work):
        """
        Get work cover with full url
        """
        current_site = Site.objects.get_current()
        return "http://{}{}".format(current_site, work.cover.url)

    class Meta:
        model = Work