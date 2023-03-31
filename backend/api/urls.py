from django.urls import include, path
from rest_framework import routers

from api.views import (TagsViewSet, RecipesViewSet, IngredientsViewSet,
                       ShoppingCartViewSet, FavoriteViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes/(?P<recipes_id>\d+)/shopping_cart',
                   ShoppingCartViewSet, basename='shopping_cart')
router_v1.register(r'recipes/(?P<recipes_id>\d+)/favorite',
                   FavoriteViewSet, basename='favorite')
# router_v1.register(r'recipes/download_shopping_cart',
#                    DownloadViewSet, basename='download')

urlpatterns = [
    path('', include(router_v1.urls)),
]
