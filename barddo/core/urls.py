from django.conf.urls import patterns, url
from .views import index, profile, editable_profile
from .views import artist_dashboard, render_collection_modal, render_work_modal

urlpatterns = patterns(
    '',
    url(r'^$',
        index,
        name='core.index'),

    url(r'^dashboard',
        artist_dashboard,
        name='core.dashboard'),

    url(r'^profile/(?P<pk>\d+)$',
        profile,
        name='core.profile'),

    url(r'^profile$',
        editable_profile,
        name='core.editable_profile'),

    #################
    # Custom Modals #
    #################
    url(r'^modal/collection/(?P<collection_id>\d+)',
        render_collection_modal,
        name='core.modal.collection'),

    url(r'^modal/work/(?P<work_id>\d+)',
        render_work_modal,
        name='core.modal.work'),
)