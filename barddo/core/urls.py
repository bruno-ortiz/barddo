from django.conf.urls import patterns, url
from .views import index
from .views import list_collection

urlpatterns = patterns(
    '',
    url(r'^$',
        index,
        name='core.index'),

    url(r'^collections$',
        list_collection,
        name='collections.list'),
)