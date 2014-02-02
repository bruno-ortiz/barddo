from django.conf.urls import patterns, url
from .views import index
from .views import artist_dashboard

urlpatterns = patterns(
    '',
    url(r'^$',
        index,
        name='core.index'),

    url(r'^dashboard',
        artist_dashboard,
        name='core.dashboard'),
)