from django.conf.urls import patterns, url
from feedback.views import FeedbackView

__author__ = 'jose'

urlpatterns = patterns(
    '',
    url(r'^feedback$', FeedbackView.as_view(), name='feedback'),

)