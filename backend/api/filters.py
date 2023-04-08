from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipesFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        field_name='favorite',
        method='filter_favorite'
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='shopping_cart',
        method='filter_shopping_cart'
    )
    tags = filters.CharFilter(field_name='tags__slug')
    author = filters.CharFilter(field_name='author__id')

    def filter_favorite(self, queryset, name, value):
        queryset.filter(favorite__isnull=False,
                        favorite__user=self.request.user)

    def filter_shopping_cart(self, queryset, name, value):
        return queryset.filter(shopping_cart__isnull=False,
                               shopping_cart__user=self.request.user)

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'is_in_shopping_cart',
            'tags'
        )
