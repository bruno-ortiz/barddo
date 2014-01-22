from django.conf.urls import patterns, include, url
from barddo_auth.views import logout_user, login

__author__ = 'bruno'

urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),
    url(r'logout$', logout_user, name='logout'),
    url(r'^login$', login, name='login'),
)