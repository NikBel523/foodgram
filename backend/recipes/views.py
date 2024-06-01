from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import RecipeModel


def redirect_to_recipe(request, short_link):
    """Перенаправление на полный URL рецепта по короткой ссылке."""
    recipe = get_object_or_404(RecipeModel, short_link=short_link)
    full_url = request.build_absolute_uri(f'recipes/{recipe.id}/')
    return HttpResponseRedirect(full_url)
