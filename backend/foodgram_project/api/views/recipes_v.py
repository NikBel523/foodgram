from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (FavoritedSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, TagSerializer)
from recipes.models import FavoriteModel, RecipeModel, TagModel

ERROR_TEXT_404 = 'Рецепт не найден.'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = RecipeModel.objects.all()
    serializer_class = RecipeReadSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AddFavoriteView(APIView):

    def post(self, request, recipe_id):
        user = request.user
        try:
            recipe = RecipeModel.objects.get(id=recipe_id)
        except RecipeModel.DoesNotExist:
            return Response(
                {"errors": ERROR_TEXT_404},
                status=status.HTTP_404_NOT_FOUND,
            )

        favorite, created = FavoriteModel.objects.get_or_create(
            user=user,
            recipe=recipe,
        )
        if not created:
            return Response(
                {'errors': 'Нельзя добавить рецепт повторно.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FavoritedSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        try:
            recipe = RecipeModel.objects.get(id=recipe_id)
        except RecipeModel.DoesNotExist:
            return Response(
                {'errors': ERROR_TEXT_404},
                status=status.HTTP_404_NOT_FOUND,
            )

        favorite = FavoriteModel.objects.filter(
            user=user,
            recipe=recipe,
        ).first()
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': 'В избранном нет выбранного рецепта.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
