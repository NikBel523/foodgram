from rest_framework import viewsets

from api.serializers import RecipeSerializer, RecipeWriteSerializer, TagSerializer
from recipes.models import RecipeModel, TagModel


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = RecipeModel.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeWriteSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


