from django.contrib import admin
from django.db.models import Count

from .models import Tag, Ingredient, Recipe, TagsRecipes, ListOfIngredients, \
    ShoppingCart, Favorite


class TagsRecipesAdmin(admin.TabularInline):
    model = TagsRecipes


class ListOfIngredientsAdmin(admin.TabularInline):
    model = ListOfIngredients


class RecipeAdmin(admin.ModelAdmin):
    def tags_list(self, obj):
        return list(tag for tag in obj.tag.all())

    def ingredients_list(self, obj):
        return list(ingredient for ingredient in obj.ingredients.all())

    def favorite_counts(self, obj):
        return Count(obj.favorite)

    list_display = (
        'pk', 'name', 'cooking_time',
        'ingredients_list', 'favorite_counts', 'tags_list', 'image'
    )
    list_editable = ('tags_list',)
    search_fields = ('name', 'cooking_time',)
    list_filter = ('tags_list',)
    inlines = [TagsRecipesAdmin, ListOfIngredientsAdmin]
    tags_list.short_description = 'Теги'
    ingredients_list.short_description = 'Ингредиенты'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('name',)
    list_filter = ('slug', 'color')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)

