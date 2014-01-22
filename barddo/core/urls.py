from django.conf.urls import patterns, url
from .views import logged

urlpatterns = patterns(
    '',
    url(r'^$', logged, name='core.index'),
)