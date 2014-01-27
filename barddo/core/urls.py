from django.conf.urls import patterns, url
from .views import index, profile
from .views import collection_list, create_collection

urlpatterns = patterns(
    '',
    url(r'^$',
        index,
        name='core.index'),

    url(r'^collections/create$',
        create_collection,
        name='collections.create'),

    url(r'^collections$',
        collection_list,
        name='collections.list'),

    url(r'profile$',
        profile,
        name='core.profile'),

    # url(r'profile/(?P<pk>/d+)/$',
    #     profile,
    #     name='core.profile'),
)