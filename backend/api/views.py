import io

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientsFilter, RecipesFilter
from api.serializers import (FavoriteSerializer, IngredientsSerializer,
                             PostRecipesSerializer, RecipesSerializer,
                             ShoppingCartSerializer, TagsSerializer)
from recipes.models import (Favorite, Ingredient, ListOfIngredients, Recipe,
                            ShoppingCart, Tag)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    ordering_fields = ['-pub_date']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return PostRecipesSerializer
        return RecipesSerializer

    @staticmethod
    def create_in_favorite_shopping(serializer, request, recipe_id):
        data = {
            'user': request.user,
            'recipe': recipe_id
        }
        serializer_data = serializer(
            data=data,
            context={
                'request': request
            }
        )
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save(user=request.user,
                             recipe_id=recipe_id)
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _delete(model, request, recipe_id):
        get_object_or_404(model,
                          recipe_id=recipe_id,
                          user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            url_path=r'(?P<recipe_id>\d+)/shopping_cart',
            methods=['POST'],
            permission_classes=[IsAuthenticated, ])
    def shopping_cart(self, request, recipe_id):
        return self.create_in_favorite_shopping(
            ShoppingCartSerializer, request, recipe_id
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, recipe_id):
        return self._delete(ShoppingCart, request, recipe_id)

    @action(detail=False,
            url_path=r'(?P<recipe_id>\d+)/favorite',
            methods=['POST'],
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, recipe_id):
        return self.create_in_favorite_shopping(FavoriteSerializer, request,
                                                recipe_id)

    @favorite.mapping.delete
    def delete_favorite(self, request, recipe_id):
        return self._delete(Favorite, request, recipe_id)

    @staticmethod
    def download_file(data):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('FreeSans', 'data/FreeSans.ttf'))
        p.setFont('FreeSans', 28)
        height = settings.HEIGHT
        p.drawString(
            settings.LEFT,
            height + 50,
            'Нужно купить:'
        )
        p.line(80, 740, 550, 740)
        for item in data:
            p.drawString(
                settings.LEFT,
                height,
                f'{item["ingredient__name"]} - '
                f'{item["amount_all"]}'
                f'{item["ingredient__measurement_unit"]}'
            )
            height -= 40
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shopping_cart.pdf'
        )

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request):

        shop_list = ListOfIngredients.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            amount_all=Sum('amount')
        ).order_by(
            'ingredient__name'
        )
        return self.download_file(shop_list)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter
