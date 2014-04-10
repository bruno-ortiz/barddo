from django.conf.urls import patterns, include, url

from accounts.views import logout_user, UsernamesAjaxView, profile, editable_profile


__author__ = 'bruno'

urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),

    url(r'^user/usernames$',
        UsernamesAjaxView.as_view(),
        name='accounts.usernames'),

    url(r'logout$',
        logout_user,
        name='logout'),

    url(r'^profile/(?P<pk>\d+)$',
        profile,
        name='account.profile'),

    url(r'^profile$',
        editable_profile,
        name='account.editable_profile'),
)