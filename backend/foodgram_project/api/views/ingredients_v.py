from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import IngredientFilter
from api.serializers import IngredientSerializer
from recipes.models import IngredientModel


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientModel.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter

