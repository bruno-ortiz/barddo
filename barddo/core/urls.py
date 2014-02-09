from django.conf.urls import patterns, url
from .views import index, profile, editable_profile
from .views import artist_dashboard, collection_detail

urlpatterns = patterns(
    '',
    url(r'^$',
        index,
        name='core.index'),

    url(r'^dashboard',
        artist_dashboard,
        name='core.dashboard'),

    url(r'^collection/(?P<collection_id>\d+)',
        collection_detail,
        name='core.collection'),
    
    url(r'^profile/(?P<pk>\d+)$',
        profile,
        name='core.profile'),

    url(r'^profile$',
        editable_profile,
        name='core.editable_profile'),
)