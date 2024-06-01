from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import ShoppingCartModel


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов в список покупок."""

    class Meta:
        model = ShoppingCartModel
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCartModel.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже в списке покупок.'
            )
        ]

