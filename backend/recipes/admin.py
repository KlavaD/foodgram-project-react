from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, TagsRecipes, ListOfIngredients,
                     ShoppingCart, Favorite)


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

    list_display = (
        'name', 'pk', 'author',
        'ingredients_list', 'favorite_counts', 'tags_list',
        'cooking_time', 'image'
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
