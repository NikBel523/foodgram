from django.db.models import Exists, OuterRef, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import pyshorteners
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.paginator import LimitPageNumberPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    ShoppingCartSerializer,
    ShortRecipeInfoSerializer,
    TagSerializer,
)
from api.utils import generate_shopping_cart_txt
from recipes.models import (
    FavoriteModel,
    RecipeIngredientsModel,
    RecipeModel,
    ShoppingCartModel,
    TagModel,
)

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

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        """Вывод короткой ссылки на рецепт."""
        recipe = self.get_object()
        base_url = request.build_absolute_uri('/')[:-1]
        recipe_url = f"{base_url}/recipes/{recipe.id}/"

        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(recipe_url)

        return Response({'short-link': short_url}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite(self, request, pk=None):
        """Добавление и удаление избранного."""
        if request.method == 'POST':
            return self._create_favorite_or_cart(
                FavoriteSerializer,
                pk,
                request,
            )
        elif request.method == 'DELETE':
            return self._delete_from_favorite_or_cart(
                FavoriteModel,
                pk,
                request,
            )

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        """Загрузка списка покупок."""
        ingredients = RecipeIngredientsModel.objects.filter(
            recipe_name__shoppingcart__user=request.user
        ).values(
            'name__name', 'name__measurement_unit'
        ).annotate(
            total_amount=Sum('amount')
        )

        txt_content = generate_shopping_cart_txt(ingredients)
        response = HttpResponse(txt_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="список.txt"'
        return response

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        """Добавление и удаление рецептов списка покупок."""
        if request.method == 'POST':
            return self._create_favorite_or_cart(
                ShoppingCartSerializer,
                pk,
                request,
            )
        elif request.method == 'DELETE':
            return self._delete_from_favorite_or_cart(
                ShoppingCartModel,
                pk,
                request,
            )

    # Вспомогательные методы для добавления и удаления избранного и списка
    def _delete_from_favorite_or_cart(self, model, pk, request):
        recipe = get_object_or_404(RecipeModel, id=pk)
        item = model.objects.filter(user=request.user, recipe=recipe).delete()
        if item[0]:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт не найден в списке покупок.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _create_favorite_or_cart(self, serializer_class, pk, request):
        user = request.user
        try:
            recipe = RecipeModel.objects.get(id=pk)
        except RecipeModel.DoesNotExist:
            return Response(
                {'errors': 'Рецепт не найден'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {'user': user.id, 'recipe': recipe.id}
        serializer = serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                ShortRecipeInfoSerializer(recipe).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
