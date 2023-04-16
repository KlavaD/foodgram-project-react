from django.contrib import admin


from .models import (Tag, Ingredient, Recipe, TagsRecipes, ListOfIngredients,
                     ShoppingCart, Favorite)


class ListOfIngredientsAdmin(admin.TabularInline):
    model = ListOfIngredients


class TagsRecipesAdmin(admin.TabularInline):
    model = TagsRecipes


class RecipeAdmin(admin.ModelAdmin):
    def tags_list(self, obj):
        return list(tag for tag in obj.tags.all())

    def ingredients_list(self, obj):
        return list(ingredient for ingredient in obj.ingredients.all())

    def favorite_counts(self, obj):
        return obj.favorite.count()

    list_display = (
        'name', 'pk', 'author',
        'ingredients_list', 'favorite_counts', 'tags_list',
        'cooking_time', 'image'
    )
    search_fields = ('name', 'cooking_time',)
    inlines = [ListOfIngredientsAdmin,
               TagsRecipesAdmin]
    list_filter = ('author',)
    tags_list.short_description = 'Теги'
    ingredients_list.short_description = 'Ингредиенты'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('name',)
    list_filter = ('slug', 'color')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
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
