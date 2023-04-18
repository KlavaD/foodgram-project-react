from django.urls import include, path
from rest_framework import routers

from api.views import IngredientsViewSet, RecipesViewSet, TagsViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),

]
