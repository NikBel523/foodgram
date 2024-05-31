from django.urls import include, path
from rest_framework import routers

from api.views import (
    FoodgramUserViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()
user_router_v1 = routers.DefaultRouter()

router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet, basename='recipes')
user_router_v1.register('users', FoodgramUserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include(user_router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
