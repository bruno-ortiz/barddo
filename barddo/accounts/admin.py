from django.contrib import admin

from .models import BarddoUser, BarddoUserProfile


class BarddoUserAdmin(admin.ModelAdmin):
    """
    Most common user fields on admin table
    """
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')


admin.site.register(BarddoUser, BarddoUserAdmin)


class BarddoUserProfileAdmin(admin.ModelAdmin):
    """
    Most common user profile fields on admin table
    """
    list_display = ('user', 'gender', 'language', 'country')


admin.site.register(BarddoUserProfile, BarddoUserProfileAdmin)