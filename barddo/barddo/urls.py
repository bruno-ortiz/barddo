from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

dajaxice_autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include("core.urls")),
    url(r'^', include('accounts.urls')),
    url(r'^', include('feedback.urls')),
    url(r'^', include('publishing.urls')),

    # Third Party URLs
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^shards/', include('shards.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))