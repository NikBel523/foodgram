from rest_framework import viewsets

from api.serializers import RecipeSerializer, TagSerializer
from recipes.models import RecipeModel, TagModel


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = RecipeModel.objects.all()
    serializer_class = RecipeSerializer
