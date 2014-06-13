import json

from django.contrib.auth import login
from django.http import HttpResponse
from social.apps.django_app.utils import strategy
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import BarddoUser
from feed.models import UserFeed
from .serializers import UserFeedSerializer, UserFriendsSerializer, SimpleWorkSerializer
from follow.models import Follow
from core.models import Work


class UserFeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for handling current user feed actions
    """
    model = UserFeed
    serializer_class = UserFeedSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List every feed action from authenticated user
        """
        queryset = UserFeed.objects.feed_for_user(request.user)
        serializer = UserFeedSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Disable single item retrieve
        """
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)


class UserFriendsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for handling current user followees
    """
    model = BarddoUser
    serializer_class = UserFriendsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List every followee from authenticated user
        """
        queryset = Follow.objects.following(request.user, BarddoUser)
        serializer = UserFriendsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Disable single item retrieve
        """
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)


class FavoritesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for handling user favorite works via rest
    """
    model = Work
    serializer_class = SimpleWorkSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List every favorite work
        """
        queryset = Work.objects.liked_by(request.user)
        serializer = SimpleWorkSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Disable single item retrieve
        """
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)


@strategy('social:complete')
def register_by_access_token(request, backend):
    """
    Handle social network registration and login, call it passing the
    access_token parameter like ?access_token=<token>.

    The URL entry must contain the backend
    """
    social_token = request.GET.get('access_token')
    backend = request.strategy.backend
    user = backend.do_auth(social_token)
    if user:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        result = {
            "status": "OK",
            "name": user.get_full_name().title(),
            "email": user.email,
            "avatar": request.build_absolute_uri(user.profile.avatar.url),
            "token": token.key
        }
    else:
        result = {"status": "NOK"}

    return HttpResponse(json.dumps(result), mimetype="application/json")