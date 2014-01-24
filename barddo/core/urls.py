from django.conf.urls import patterns, url
from .views import index
from .views import collection_list, collection_create

urlpatterns = patterns('',

    url(r'^$',
        index,
        name='core.index'),

    url(r'^collections/create$',
        collection_create,
        name='collections.create'),

    url(r'^collections$',
        collection_list,
        name='collections.list'),
)