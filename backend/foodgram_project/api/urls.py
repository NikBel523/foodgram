from django.urls import include, path
from rest_framework import routers

from api.views import TagViewSet

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()

router_v1.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
