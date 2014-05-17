from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    """
    Enabling feedback on the admin
    """
    pass


admin.site.register(Feedback, FeedbackAdmin)