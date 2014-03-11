from django.conf.urls import patterns, include, url

from accounts.views import logout_user, UsernamesAjaxView


__author__ = 'bruno'

urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),
    url(r'logout$', logout_user, name='logout'),
    url(r'^user/usernames$', UsernamesAjaxView.as_view(), name='user.usernames'),
)