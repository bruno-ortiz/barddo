from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    """
    Enabling feedback on the admin
    """
    list_display = ('name', 'email', 'feedback', 'date')
    ordering = ['-date']


admin.site.register(Feedback, FeedbackAdmin)