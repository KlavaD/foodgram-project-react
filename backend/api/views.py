from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.filters import RecipesFilter
from api.mixins import CreateDestroyViewSet
from api.serializers import (TagsSerializer, RecipesSerializer,
                             PostRecipesSerializer, ShoppingCartSerializer,
                             FavoriteSerializer, IngredientsSerializer)
from recipes.models import (Tag, Recipe, ShoppingCart, Ingredient,
                            ListOfIngredients)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    ordering_fields = ['-id']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return PostRecipesSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer


class ShoppingCartViewSet(CreateDestroyViewSet):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        return self.request.user.shopping_cart.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return self.request.user.favorite.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class DownloadViewSet():
#     pass
