from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Follow


class UserAdmin(BaseUserAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
