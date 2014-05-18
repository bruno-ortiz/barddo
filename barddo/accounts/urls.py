from django.conf.urls import patterns, include, url

from accounts.views import LogoutView, UsernamesAjaxView, UserProfileView


urlpatterns = patterns(
    '',
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^user/usernames$',
        UsernamesAjaxView.as_view(),
        name='accounts.usernames'),

    url(r'logout$',
        LogoutView.as_view(),
        name='logout'),

    url(r'^profile/(?P<pk>\d+)$',
        UserProfileView.as_view(),
        name='account.profile'),

    url(r'^profile$',
        UserProfileView.as_view(editable=True),
        name='account.editable_profile'),
)