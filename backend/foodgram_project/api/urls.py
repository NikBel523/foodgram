from django.urls import include, path
from rest_framework import routers

from api.views import (AddFavoriteView, AvatarChangeView, IngredientViewSet,
                       RecipeViewSet, SubscribeView, SubscriptionListView,
                       TagViewSet)

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()

router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet)


custom_users_urls = [
    path(
        'subscriptions/',
        SubscriptionListView.as_view(),
        name='subscription-list',
    ),
    path('<int:id>/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('me/avatar/', AvatarChangeView.as_view(), name='avatar-patch'),
]


urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'recipes/<int:recipe_id>/favorite/',
        AddFavoriteView.as_view(),
        name='add_favorite',
    ),
    path('users/', include(custom_users_urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
