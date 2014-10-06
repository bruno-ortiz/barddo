from django.conf.urls import patterns, url

from core.views import ArtistBankAccountView, CollectionPageView
from .views import index, AboutUsView, TermsView, HelpView, WorkPageView, ArtistStatisticsView
from .views import artist_dashboard, upload_work_page, move_work_page, remove_work_page


urlpatterns = patterns(
    '',
    url(r'^/?$',
        index,
        name='core.index'),

    url(r'^dashboard$',
        artist_dashboard,
        name='core.dashboard'),

    url(r'^dashboard/statistics$',
        ArtistStatisticsView.as_view(),
        name='core.statistics'),

    url(r'^dashboard/bank/account$',
        ArtistBankAccountView.as_view(),
        name='core.bank.account'),

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

    url(r'^help$',
        HelpView.as_view(),
        name='core.help'),

    url(r'^about-us$',
        AboutUsView.as_view(),
        name='core.about'),

    url(r'^terms',
        TermsView.as_view(),
        name='core.terms'),

    url(r'^work/(?P<work_id>\d+)/?.*$',
        WorkPageView.as_view(),
        name='core.work.detail'),

    url(r'^collection/(?P<collection_slug>[\w_-]+)$',
        CollectionPageView.as_view(),
        name='core.collection.detail')

)