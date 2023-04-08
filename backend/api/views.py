from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import RecipesFilter
from api.mixins import CreateDestroyViewSet
from api.serializers import (TagsSerializer, RecipesSerializer,
                             PostRecipesSerializer, ShoppingCartSerializer,
                             FavoriteSerializer, IngredientsSerializer)
from recipes.models import (Tag, Recipe, ShoppingCart, Ingredient,
                            ListOfIngredients, Favorite)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    # pagination_class =[None,]
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
    pagination_class = None
    serializer_class = IngredientsSerializer
    search_fields = ('^name',)


class ShoppingCartView(APIView):
    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        data = {'user': self.request.user,
                'recipe': recipe
                }
        serializer = ShoppingCartSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,
                            recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        ShoppingCart.objects.get(recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteView(APIView):

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        data = {'user': self.request.user,
                'recipe': recipe
                }
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,
                            recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        Favorite.objects.get(recipe_id=recipe_id,
                             user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class DownloadViewSet():
#     pass
