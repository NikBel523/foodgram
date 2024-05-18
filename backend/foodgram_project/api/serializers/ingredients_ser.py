from rest_framework import serializers

from recipes.models import IngredientModel


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientModel
        fields = ('id', 'name', 'measurement_unit',)
