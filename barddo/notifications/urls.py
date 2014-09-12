# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns('notifications.views',
                       url(r'^$', 'all', name='all'), )
