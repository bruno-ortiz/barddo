from django.contrib import admin

from .models import UserContact


class UserContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserContact, UserContactAdmin)