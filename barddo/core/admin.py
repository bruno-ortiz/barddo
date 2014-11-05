from django.contrib import admin

from .models import Collection, Work, CollectionAvailability


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


class CollectionAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('collection', 'modify_date', 'status')


admin.site.register(CollectionAvailability, CollectionAvailabilityAdmin)