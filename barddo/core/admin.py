from django.contrib import admin

from .models import CollectionUnit, Collection, Work


class CollectionUnitAdmin(admin.ModelAdmin):
    """
    Simple collection unit admin view
    """
    pass


admin.site.register(CollectionUnit, CollectionUnitAdmin)


class CollectionAdmin(admin.ModelAdmin):
    """
    Most common collection fields on admin table
    """
    list_display = ('name', 'status', 'unit', 'author')


admin.site.register(Collection, CollectionAdmin)


class WorkAdmin(admin.ModelAdmin):
    """
    Most common work fields on admin table
    """
    list_display = ('collection', 'title', 'unit_count', 'total_pages')


admin.site.register(Work, WorkAdmin)