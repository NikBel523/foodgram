from django.db.models import Exists, OuterRef, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.paginator import LimitPageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    ShoppingCartSerializer,
    ShortRecipeInfoSerializer,
    TagSerializer,
)
from api.utils import generate_shopping_cart_txt
from foodgram_project.settings import SHORT_URL_PREFIX
from recipes.models import (
    FavoriteModel,
    RecipeIngredientsModel,
    RecipeModel,
    ShoppingCartModel,
    TagModel,
)


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
    permission_classes = (IsAuthorOrReadOnly,)

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
        short_url = f'{base_url}/{SHORT_URL_PREFIX}/{recipe.short_link}/'

        return Response({'short-link': short_url}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='favorite')
    def favorite(self, request, pk):
        """Добавление избранного."""
        if request.method == 'POST':
            return self._create_favorite_or_cart(
                FavoriteSerializer,
                pk,
                request,
            )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление избранного."""
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

    @action(detail=True, methods=['post'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        """Добавление рецептов списка покупок."""
        if request.method == 'POST':
            return self._create_favorite_or_cart(
                ShoppingCartSerializer,
                pk,
                request,
            )

    @shopping_cart.mapping.delete
    def delete_shopping_cart_recipe(self, request, pk):
        """Удаление рецептов списка покупок."""
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
        recipe = get_object_or_404(RecipeModel, id=pk)

        data = {'user': user.id, 'recipe': recipe.id}
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            ShortRecipeInfoSerializer(recipe).data,
            status=status.HTTP_201_CREATED,
        )
