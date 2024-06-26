from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import IngredientFilter
from api.serializers import IngredientSerializer
from recipes.models import IngredientModel


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ВьюСет для модели ингредиентов."""

    queryset = IngredientModel.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
