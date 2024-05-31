from rest_framework import serializers

from recipes.models import IngredientModel


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор обработки ингрдиентов."""

    class Meta:
        model = IngredientModel
        fields = ('id', 'name', 'measurement_unit',)
