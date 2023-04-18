from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User, Follow


class UserAdmin(BaseUserAdmin):
    @admin.display(description='Кол-во рецептов у пользователя')
    def count_recipes(self, obj):
        return obj.recipes.count()

    @admin.display(description='Кол-во подписчиков у пользователя')
    def count_followers(self, obj):
        return obj.follower.count()

    list_display = (
        'username', 'pk', 'email', 'first_name', 'last_name',
        'count_recipes', 'count_followers'
    )
    search_fields = ('username', 'email',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.unregister(Group)
