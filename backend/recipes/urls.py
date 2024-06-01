from django.urls import path

from .views import redirect_to_recipe

app_name = 'recipes'

urlpatterns = [
    path(
        'recipes/<str:short_link>/',
        redirect_to_recipe,
        name='redirect-to-recipe',
    ),
]
