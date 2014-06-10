from rest_framework.serializers import ModelSerializer, DateTimeField, CharField

from feed.models import UserFeed


class UserFeedSerializer(ModelSerializer):
    created = DateTimeField(read_only=True)
    picture = CharField(source="get_picture", read_only=True)
    message = CharField(source="get_message", read_only=True)

    class Meta:
        model = UserFeed