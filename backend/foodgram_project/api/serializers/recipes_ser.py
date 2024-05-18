from rest_framework import serializers

from recipes.models import TagModel


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'slug',)
