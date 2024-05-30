from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ShortRecipeInfoSerializer
from api.utils import generate_shopping_cart_txt
from recipes.models import RecipeModel, ShoppingCartModel


class DownloadShoppingCartView(APIView):
    """Вью для скачивания списка покупок."""

    def get(self, request):
        cart_items = ShoppingCartModel.objects.filter(user=request.user)
        ingredients = {}

        for item in cart_items:
            for ingredient in item.recipe.recipeingredients.all():
                ingredient_name = ingredient.name.name
                measurement_unit = ingredient.name.measurement_unit

                if ingredient_name in ingredients:
                    ingredients[ingredient_name]['amount'] += ingredient.amount
                else:
                    ingredients[ingredient_name] = {
                        'amount': ingredient.amount,
                        'measurement_unit': measurement_unit,
                    }

        txt_content = generate_shopping_cart_txt(ingredients)
        response = HttpResponse(txt_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="список.txt"'
        return response


class ManageShoppingCartView(APIView):
    """Вью для управления рецептами в списке покупок."""

    def post(self, request, recipe_id):
        try:
            recipe = RecipeModel.objects.get(id=recipe_id)
        except RecipeModel.DoesNotExist:
            return Response(
                {'errors': 'Рецепт не найден'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart_item, created = ShoppingCartModel.objects.get_or_create(
            user=request.user,
            recipe=recipe,
        )
        if not created:
            return Response(
                {'errors': 'Рецепт уже в корзине.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ShortRecipeInfoSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(RecipeModel, id=recipe_id)
        try:
            cart_item = ShoppingCartModel.objects.get(
                recipe=recipe.id,
                user=request.user,
            )
        except ShoppingCartModel.DoesNotExist:
            return Response(
                {'errors': 'Рецепта не было в вашей корзине.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
