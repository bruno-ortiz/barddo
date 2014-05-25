from django.contrib import admin

from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    """
    Most common ratings fields on admin table
    """
    list_display = ('user', 'work', 'like')


admin.site.register(Rating, RatingAdmin)
