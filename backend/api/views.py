from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_pdf.response import PDFResponse, PDFFileResponse
from drf_pdf.renderer import PDFRenderer

from api.filters import RecipesFilter, IngredientsFilter
from api.serializers import (TagsSerializer, RecipesSerializer,
                             PostRecipesSerializer, ShoppingCartSerializer,
                             FavoriteSerializer, IngredientsSerializer)
from recipes.models import (Tag, Recipe, ShoppingCart, Ingredient,
                            Favorite)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    ordering_fields = ['-id']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return PostRecipesSerializer
        return RecipesSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter


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


class DownloadShopList(APIView):

    def get(self, request):
        shop_list = ShoppingCart.objects.filter(
            user=request.user
        ).values(
            'recipe__ingredients__name',
            'recipe__recipe_ingredients__amount',
            'recipe__ingredients__measurement_unit'
        ).annotate(amount=Sum('recipe__recipe_ingredients__amount')).order_by(
            'recipe__ingredients__name'
        )
        data = []

        for item in shop_list:
            data.append(
                f'{item["recipe__ingredients__name"]}-'
                f'{item["recipe__recipe_ingredients__amount"]}\t'
                f'{item["recipe__ingredients__measurement_unit"]} \n')
        response = HttpResponse(
            data,
            headers={
                'content-type': 'text/plain',
                'Content-Disposition': 'attachment; filename="shopping_cart.txt'
            },
            status=status.HTTP_200_OK
        )
        return response
