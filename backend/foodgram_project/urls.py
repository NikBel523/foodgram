from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api_v1')),
    # path('', include('recipes.urls', namespace='recipes')),

]