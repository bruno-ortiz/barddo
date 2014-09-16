# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor',
                    'target', 'unread')
    list_filter = ('unread', 'timestamp', )


admin.site.register(Notification, NotificationAdmin)
