from django.conf.urls import patterns, url

from .views import index, profile, editable_profile
from .views import artist_dashboard, upload_work_page, move_work_page


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

    url(r'^work/page/upload/(?P<work_id>\d+)$',
        upload_work_page,
        name='core.upload.work.page'),

    url(r'^work/page/upload$',
        upload_work_page,
        name='core.upload.work.page'),

    url(r'^work/page/order/(?P<work_id>\d+)',
        move_work_page,
        name='core.move.work.page'),
)