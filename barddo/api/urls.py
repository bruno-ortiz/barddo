from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from .views import register_by_access_token, UserFeedViewSet, UserFriendsViewSet, FavoritesViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'feed', UserFeedViewSet)
router.register(r'friends', UserFriendsViewSet)
router.register(r'favorites', FavoritesViewSet)

urlpatterns = patterns(
    '',

    url(r'^', include(router.urls)),

    url(r'^token/register/(?P<backend>[^/]+)/$',
        register_by_access_token,
        name='register.token'),

    url(r'', include('rest_framework.urls', namespace='rest_framework'))
)