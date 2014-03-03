from django.conf.urls import patterns, include, url

from publishing.views import publisher_landpage


__author__ = 'bruno'

urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),
    url(r'publisher$', publisher_landpage, name='publishing.landpage'),
)