from django.conf.urls import patterns, url

from search.views import search_result


urlpatterns = patterns(
    '',
    url(r'^search/', search_result, name='search.result'),
)