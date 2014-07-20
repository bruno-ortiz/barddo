from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from shards.core import shards_autodiscover
from barddo.receivers import receivers_autodiscover


receivers_autodiscover()

shards_autodiscover()

admin.autodiscover()

dajaxice_autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include("core.urls")),
    url(r'^', include('accounts.urls')),
    url(r'^', include('feedback.urls')),
    url(r'^', include('publishing.urls')),
    url(r'^', include('search.urls')),
    url(r'^', include('payments.urls')),


    url(r'^api/', include('api.urls')),

    # Third Party URLs
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^shards/', include('shards.urls')),

    # Internationalization
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # Custom Metrics
    url(r'^metrics/', include('redis_metrics.urls')), # Enable when secure
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
