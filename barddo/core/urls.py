from django.conf.urls import patterns, url

from .views import index, AboutUsView, FeaturesView
from .views import artist_dashboard, upload_work_page, move_work_page, remove_work_page


urlpatterns = patterns(
    '',
    url(r'^$',
        index,
        name='core.index'),

    url(r'^dashboard',
        artist_dashboard,
        name='core.dashboard'),

    url(r'^work/page/upload/(?P<work_id>\d+)$',
        upload_work_page,
        name='core.upload.work.page'),

    url(r'^work/page/upload$',
        upload_work_page,
        name='core.upload.work.page'),

    url(r'^work/page/order/(?P<work_id>\d+)',
        move_work_page,
        name='core.move.work.page'),

    url(r'^work/(?P<work_id>\d+)/page/(?P<page_index>\d+)/remove',
        remove_work_page,
        name='core.remove.work.page'),

    url(r'^about-us$',
        AboutUsView.as_view(),
        name='core.about'),

    url(r'^features$',
        FeaturesView.as_view(),
        name='core.features'),
)