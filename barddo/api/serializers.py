from rest_framework.serializers import ModelSerializer, DateTimeField, CharField, SerializerMethodField
from django.contrib.sites.models import Site

from feed.models import UserFeed
from accounts.models import BarddoUser
from core.models import Work


class UserFeedSerializer(ModelSerializer):
    created = DateTimeField(read_only=True)
    picture = CharField(source="get_picture", read_only=True)
    message = CharField(source="get_message", read_only=True)

    class Meta:
        model = UserFeed


class UserFriendsSerializer(ModelSerializer):
    id = CharField(source="id", read_only=True)
    name = CharField(source="get_full_name", read_only=True)
    picture = SerializerMethodField("get_avatar_url")

    def get_avatar_url(self, user):
        current_site = Site.objects.get_current()
        return "http://{}{}".format(current_site, user.profile.avatar.url)

    class Meta:
        model = BarddoUser


class SimpleWorkSerializer(ModelSerializer):
    id = CharField(source="id", read_only=True)
    title = CharField(source="title", read_only=True)
    author = CharField(source="author.get_full_name", read_only=True)
    cover = SerializerMethodField("get_cover_url")

    def get_cover_url(self, work):
        current_site = Site.objects.get_current()
        return "http://{}{}".format(current_site, work.cover.url)

    class Meta:
        model = Work