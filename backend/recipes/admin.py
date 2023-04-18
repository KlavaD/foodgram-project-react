from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, ListOfIngredients, Recipe,
                     ShoppingCart, Tag, TagsRecipes)


class ListOfIngredientsAdmin(admin.TabularInline):
    model = ListOfIngredients
    min_num = 1


class TagsRecipesAdmin(admin.TabularInline):
    model = TagsRecipes
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    @admin.display(description='тэги')
    def tags_list(self, obj):
        return list(tag for tag in obj.tags.all())

    @admin.display(description='ингредиенты')
    def ingredients_list(self, obj):
        return list(ingredient for ingredient in obj.ingredients.all())

    @admin.display(description='В избранном')
    def favorite_counts(self, obj):
        return obj.favorite.count()

    @admin.display(description='Фото')
    def take_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')

    list_display = (
        'name', 'pk', 'author', 'take_image',
        'ingredients_list', 'favorite_counts', 'tags_list',
        'cooking_time'
    )
    search_fields = ('name', 'cooking_time',)
    list_filter = ('author',)
    inlines = [ListOfIngredientsAdmin,
               TagsRecipesAdmin]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('name',)
    list_filter = ('slug', 'color')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'
