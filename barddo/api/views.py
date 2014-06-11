import json

from django.contrib.auth import login
from django.http import HttpResponse
from social.apps.django_app.utils import strategy
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from accounts.models import BarddoUser
from feed.models import UserFeed
from .serializers import UserFeedSerializer, UserFriendsSerializer, SimpleWorkSerializer
from follow.models import Follow
from core.models import Work


class UserFeedViewSet(viewsets.ReadOnlyModelViewSet):
    model = UserFeed
    serializer_class = UserFeedSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = UserFeed.objects.feed_for_user(request.user)
        serializer = UserFeedSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = UserFeed.objects.feed_for_user(request.user)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserFeedSerializer(user)
        return Response(serializer.data)


class UserFriendsViewSet(viewsets.ReadOnlyModelViewSet):
    model = BarddoUser
    serializer_class = UserFriendsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Follow.objects.following(request.user, BarddoUser)
        serializer = UserFriendsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Follow.objects.following(request.user, BarddoUser)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserFriendsSerializer(user)
        return Response(serializer.data)


class FavoritesViewSet(viewsets.ReadOnlyModelViewSet):
    model = Work
    serializer_class = SimpleWorkSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Work.objects.liked_by(request.user)
        serializer = SimpleWorkSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Work.objects.liked_by(request.user)
        work = get_object_or_404(queryset, pk=pk)
        serializer = SimpleWorkSerializer(work)
        return Response(serializer.data)


# Define an URL entry to point to this view, call it passing the
# access_token parameter like ?access_token=<token>. The URL entry must
# contain the backend, like this:
#
#   url(r'^register-by-token/(?P<backend>[^/]+)/$',
#       'register_by_access_token')

@strategy('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter
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