from django.urls import include, path
from rest_framework import routers

from api.views import (TagsViewSet, RecipesViewSet, IngredientsViewSet,
                       ShoppingCartView, FavoriteView)

router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
# router_v1.register(r'recipes/download_shopping_cart',
#                    DownloadViewSet, basename='download')

urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartView.as_view(), name='shopping_cart'),

    path('recipes/<int:recipe_id>/favorite/',
         FavoriteView.as_view(), name='favorite'),

    path('', include(router_v1.urls)),

]
