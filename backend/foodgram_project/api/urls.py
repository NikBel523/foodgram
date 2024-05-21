from django.urls import include, path
from rest_framework import routers

from api.views import AvatarChangeView, IngredientViewSet, TagViewSet, RecipeViewSet

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()

router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'recipes', RecipeViewSet)
# router_v1.register('users/me/avatar', AvatarChangeView)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('users/me/avatar/', AvatarChangeView.as_view(), name='avatar-patch'),
    path('auth/', include('djoser.urls.authtoken')),
]
