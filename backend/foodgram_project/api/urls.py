from django.urls import include, path
from rest_framework import routers

from api.views import (AddFavoriteView, AvatarChangeView, IngredientViewSet,
                       RecipeViewSet, SubscribeView, SubscriptionListView,
                       TagViewSet)

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()

router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'recipes', RecipeViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path(
        'recipes/<int:recipe_id>/favorite/',
        AddFavoriteView.as_view(),
        name='add_favorite',
    ),
    path(
        'users/subscriptions/',
        SubscriptionListView.as_view(),
        name='subscription-list',
    ),
    path('users/<int:id>/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('users/me/avatar/', AvatarChangeView.as_view(), name='avatar-patch'),
    path('auth/', include('djoser.urls.authtoken')),
]
