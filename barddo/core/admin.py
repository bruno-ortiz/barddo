from django.contrib import admin
from .models import CollectionUnit


class CollectionUnitAdmin(admin.ModelAdmin):
    pass
admin.site.register(CollectionUnit, CollectionUnitAdmin)