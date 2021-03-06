from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from .views import register_by_access_token, UserFeedViewSet, PageRetrieve, UserFriendsViewSet, FavoritesViewSet, WorksViewSet, WorkSearchViewSet, CompleteWorkViewSet


router = DefaultRouter()

# User actions feed
router.register(r'feed', UserFeedViewSet, base_name="user-feed")

# User friends list
router.register(r'friends', UserFriendsViewSet, base_name="user-friends")

# User favorite works
router.register(r'favorites', FavoritesViewSet, base_name="user-favorites")

router.register(r'work', CompleteWorkViewSet, base_name="work")

router.register(r'works', WorksViewSet, base_name="works")

router.register(r'search-work', WorkSearchViewSet, base_name="search-work")

urlpatterns = patterns(
    '',

    url(r'^work/(?P<work_id>\d+)/page/(?P<page_number>\d+)/',
        PageRetrieve.as_view(),
        name='work_page'),

    url(r'^', include(router.urls)),

    url(r'^token/register/(?P<backend>[^/]+)/$',
        register_by_access_token,
        name='register.token'),

    url(r'', include('rest_framework.urls', namespace='rest_framework'))
)