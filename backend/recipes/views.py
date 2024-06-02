from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import RecipeModel
from foodgram_project.settings import DOMAIN_NAME


def redirect_to_recipe(request, short_link):
    """Перенаправление на полный URL рецепта по короткой ссылке."""
    recipe = get_object_or_404(RecipeModel, short_link=short_link)
    full_url = f'https://{DOMAIN_NAME}/recipes/{recipe.id}/'
    return HttpResponseRedirect(full_url)
