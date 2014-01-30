from django.conf.urls import patterns, include, url
from accounts.views import logout_user

__author__ = 'bruno'

urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),
    url(r'logout$', logout_user, name='logout'),
)