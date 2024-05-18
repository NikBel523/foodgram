from rest_framework import viewsets

from api.serializers import IngredientSerializer
from recipes.models import IngredientModel


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientModel.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
