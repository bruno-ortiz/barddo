import json
import os

from PIL import Image
from django.contrib.auth import login
from django.http import HttpResponse
from django.conf import settings
from social.apps.django_app.utils import strategy
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.html import escape
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from easy_thumbnails.files import get_thumbnailer

from accounts.models import BarddoUser
from feed.models import UserFeed
from .serializers import UserFeedSerializer, UserFriendsSerializer, SimpleWorkSerializer, LikedWorkSerializer, CompleteWorkSerializer
from follow.models import Follow
from core.models import Work
from core.views import IndexView
from search.views import SearchResultView


class WorkSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for handling current user feed actions
    """
    model = Work
    serializer_class = SimpleWorkSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        """
        Work search
        """
        delegate_view = SearchResultView()
        query = delegate_view.parse_search_criteria(escape(self.request.QUERY_PARAMS.get('q', None)))
        result = {}

        if query:
            queryset = delegate_view.search_in_works(query)
            result = SimpleWorkSerializer(queryset, many=True).data

        return Response(result)


class CompleteWorkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for handling current user feed actions
    """
    model = Work
    permission_classes = [AllowAny]

    def list(self, request):
        """
        Work search
        """
        delegate_view = SearchResultView()
        query = delegate_view.parse_search_criteria(escape(self.request.QUERY_PARAMS.get('q', None)))
        result = {}

        if query:
            queryset = delegate_view.search_in_works(query)
            result = SimpleWorkSerializer(queryset, many=True).data

        return Response(result)

    def retrieve(self, request, pk=None):
        """
        Single work data retrieve
        """
        queryset = Work.objects.all()
        work = get_object_or_404(queryset, pk=pk)
        serializer = CompleteWorkSerializer(work)
        return Response(serializer.data)


class WorksViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for handling current user feed actions
    """
    model = Work
    serializer_class = SimpleWorkSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        """
        List every work displayed on main page
        """
        queryset = IndexView().get_new_works(request.user)
        new_works = LikedWorkSerializer(queryset, many=True).data

        queryset = IndexView().get_rising_works(request.user)
        rising_works = LikedWorkSerializer(queryset, many=True).data

        queryset = IndexView().get_trending_works(request.user)
        trending_works = LikedWorkSerializer(queryset, many=True).data

        result = {
            'rising': rising_works,
            'trending': trending_works,
            'new': new_works
        }

        return Response(result)

    def retrieve(self, request, pk=None):
        """
        Disable single item retrieve
        """
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)


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


class PageRetrieve(APIView):
    """
    Work pages retrieving
    """
    #authentication_classes = (TokenAuthentication,) # TODO: enable authentication mode
    permission_classes = (AllowAny, )

    # TODO: centralize this validation
    @staticmethod
    def can_read(user, work):
        return work.is_free() or work.is_owned_by(user) or user.is_staff or work.author == user

    def get(self, request, work_id, page_number):
        work = Work.objects.get(pk=int(work_id))

        if not PageRetrieve.can_read(request.user, work):
            with open(os.path.join(settings.MEDIA_ROOT, 'system', 'not_found_page.png'), "rb") as f:
                return HttpResponse(f.read(), mimetype="image/png")

        if int(page_number) >= len(work.pages):
            with open(os.path.join(settings.MEDIA_ROOT, 'system', 'not_found_page.png'), "rb") as f:
                return HttpResponse(f.read(), mimetype="image/png")

        try:
            image_file = get_thumbnailer(work.pages[int(page_number)].image)['reader_image'].file
            # TODO: use python magic to detect mimetype
            return HttpResponse(image_file.read(), mimetype="image/png")
        except IOError:
            # Fallback
            red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
            response = HttpResponse(mimetype="image/jpeg")
            red.save(response, "JPEG")
            return response


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