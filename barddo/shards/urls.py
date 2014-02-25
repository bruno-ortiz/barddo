try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from .views import ShardRequest

urlpatterns = patterns(
    'shards.views',
    url(r'^(.+)/$', ShardRequest.as_view(), name='shards-call-endpoint'),
    url(r'', ShardRequest.as_view(), name='shards-endpoint'),
)