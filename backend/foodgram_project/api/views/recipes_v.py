import pyshorteners
from django.db.models import BooleanField, Exists, OuterRef, Value
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import RecipeFilter
from api.paginator import LimitPageNumberPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (FavoritedSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, TagSerializer)
from recipes.models import (FavoriteModel, RecipeModel, ShoppingCartModel,
                            TagModel)

ERROR_TEXT_400 = 'Рецепт не существует.'
ERROR_TEXT_404 = 'Рецепт не найден.'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов и создания коротких ссылок на них."""

    serializer_class = RecipeReadSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        queryset = RecipeModel.objects.all()

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(
                    FavoriteModel.objects.filter(
                        recipe=OuterRef('id'),
                        user=user,
                    )
                ),
                is_in_shopping_cart=Exists(
                    ShoppingCartModel.objects.filter(
                        recipe=OuterRef('id'),
                        user=user,
                    )
                )
            )
        # else:
        #     queryset = queryset.annotate(
        #         is_favorited=Value(False, output_field=BooleanField()),
        #         is_in_shopping_cart=Value(False, output_field=BooleanField())
        #     )

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        base_url = request.build_absolute_uri('/')[:-1]
        recipe_url = f"{base_url}/recipes/{recipe.id}/"

        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(recipe_url)

        return Response({'short-link': short_url}, status=status.HTTP_200_OK)


class AddFavoriteView(APIView):
    """Вью для добавления и удаления избранного."""

    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def post(self, request, recipe_id):
        user = request.user
        try:
            recipe = RecipeModel.objects.get(id=recipe_id)
        except RecipeModel.DoesNotExist:
            return Response(
                {"errors": ERROR_TEXT_400},
                status=status.HTTP_400_BAD_REQUEST,
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
