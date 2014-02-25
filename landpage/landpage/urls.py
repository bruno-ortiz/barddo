from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.index', name='home'),
    url(r'^stats/', include(admin.site.urls)),
)
