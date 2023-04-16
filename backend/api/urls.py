from django.urls import include, path
from rest_framework import routers

from api.views import (TagsViewSet, RecipesViewSet, IngredientsViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [

    path('', include(router_v1.urls)),

]
