from django.contrib import admin

from .models import Collection, Work


class CollectionAdmin(admin.ModelAdmin):
    """
    Most common collection fields on admin table
    """
    list_display = ('name', 'status', 'author')


admin.site.register(Collection, CollectionAdmin)


class WorkAdmin(admin.ModelAdmin):
    """
    Most common work fields on admin table
    """
    list_display = ('collection', 'title', 'unit_count', 'total_pages')


admin.site.register(Work, WorkAdmin)