from django.conf.urls import patterns, url

from .views import publisher_landpage, JoinBarddoModal, CountriesAjaxView, CreateGroupModal


__author__ = 'bruno'

urlpatterns = patterns(
    '',
    url(r'publisher$', publisher_landpage, name='publishing.landpage'),
    url(r'^profile$', JoinBarddoModal.as_view()),  # TODO: temporary url, because the autodiscover doesnt work with shards.
    url(r'^profile$', CreateGroupModal.as_view()),  # TODO: temporary url, because the autodiscover doesnt work with shards.
    url(r'publisher/countries$', CountriesAjaxView.as_view(), name='publisher.countries'),

)