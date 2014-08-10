from rest_framework.serializers import ModelSerializer, DateTimeField, CharField, SerializerMethodField, IntegerField, Serializer
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
        fields = ('id', 'title', 'author', 'cover')


class WorkPagesSerializer(Serializer):
    """
    Serializer for a few fields on user favorite works, user for work list
    """
    summary = SerializerMethodField("get_pages")

    def get_pages(self, work):
        """
        Get work pages full url in sequence order
        """
        current_site = Site.objects.get_current()
        page_list = ["http://{}{}".format(current_site, entry.image.url) for entry in work.pages]

        return page_list


class CompleteWorkSerializer(SimpleWorkSerializer):
    """
    Serializer for a few fields on user favorite works, user for work list
    """
    summary = CharField(source="summary", read_only=True)
    publish_date = DateTimeField(source="publish_date", read_only=True)
    pages_count = SerializerMethodField("get_pages_count")

    def get_pages_count(self, work):
        return work.work_pages.count()

    def get_pages(self, work):
        """
        Get work pages full url in sequence order
        """
        current_site = Site.objects.get_current()
        page_list = ["http://{}{}".format(current_site, entry.image.url) for entry in work.pages]

        return page_list

    class Meta:
        model = Work
        fields = ('id', 'title', 'author', 'cover', 'summary', 'publish_date', 'pages_count')


class LikedWorkSerializer(SimpleWorkSerializer):
    """
    Serializer for a few fields on user favorite works, user for work list
    """

    liked = SerializerMethodField("was_liked_by_user")

    def was_liked_by_user(self, work):
        return work.liked == 1

    class Meta:
        model = Work
        fields = ('id', 'title', 'author', 'cover', 'liked')