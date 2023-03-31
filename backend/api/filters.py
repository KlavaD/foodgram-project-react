from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipesFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        method='filter_favorite'
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_shopping_cart'
    )
    tags = filters.CharFilter(field_name='tag__slug')

    def filter_favorite(self, queryset, name, value):
        return queryset.filter(is_favorite__isnull=False)

    def filter_shopping_cart(self, queryset, name, value):
        return queryset.filter(is_in_shopping_cart__isnull=False)

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'is_in_shopping_cart',
            'tags'
        )
