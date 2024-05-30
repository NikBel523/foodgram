from django.urls import include, path
from rest_framework import routers

from api.views import (
    AddFavoriteView,
    DownloadShoppingCartView,
    FoodgramUserViewSet,
    IngredientViewSet,
    ManageShoppingCartView,
    RecipeViewSet,
    SubscribeView,
    TagViewSet,
)

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()
user_router_v1 = routers.DefaultRouter()

router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet, basename='recipes')
user_router_v1.register(r'users', FoodgramUserViewSet, basename='users')

# urls для дополнительного функционала пользователей
custom_users_urls = [
    path('<int:id>/subscribe/', SubscribeView.as_view(), name='subscribe'),
]

# urls для дополнительного функционала в рецептах
recipes_urls = [
    path(
        'download_shopping_cart/',
        DownloadShoppingCartView.as_view(),
        name='download_shopping_cart',
    ),
    path(
        '<int:recipe_id>/favorite/',
        AddFavoriteView.as_view(),
        name='add_favorite',
    ),
    path(
        '<int:recipe_id>/shopping_cart/',
        ManageShoppingCartView.as_view(),
        name='add_to_shopping_cart',
    ),
]


urlpatterns = [
    path('recipes/', include(recipes_urls)),
    path('', include(router_v1.urls)),
    path('users/', include(custom_users_urls)),
    path('', include(user_router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
