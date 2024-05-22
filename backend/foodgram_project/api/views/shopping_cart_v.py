from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from api.serializers import FavoritedSerializer
from recipes.models import ShoppingCartModel, RecipeModel, TagModel


class DownloadShoppingCartView(APIView):
    ...


class ManageShoppingCartView(APIView):

    def post(self, request, recipe_id):
        recipe = get_object_or_404(RecipeModel, id=recipe_id)
        cart_item, created = ShoppingCartModel.objects.get_or_create(
            user=request.user,
            recipe=recipe,
        )
        if not created:
            return Response(
                {'errors': 'Рецепт уже в корзине.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FavoritedSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):

        cart_item = ShoppingCartModel.objects.filter(recipe=recipe_id)
        if cart_item:
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепта не было в корзине.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
