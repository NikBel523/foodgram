from rest_framework import viewsets

from api.serializers import TagSerializer
from recipes.models import TagModel


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
