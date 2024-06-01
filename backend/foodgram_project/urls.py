from django.contrib import admin
from django.urls import include, path

from .settings import SHORT_URL_PREFIX

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api_v1')),
    path(f'{SHORT_URL_PREFIX}/', include('recipes.urls', namespace='recipes')),
]
