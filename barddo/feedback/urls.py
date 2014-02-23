from django.conf.urls import patterns, url

from views import FeedbackModalView


__author__ = 'jose'

urlpatterns = patterns(
    'feedback.views',
    url(r'^profile$',
        FeedbackModalView.as_view()),
)