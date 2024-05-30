from rest_framework import serializers

from recipes.models import ShoppingCartModel


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов в список покупок."""

    class Meta:
        model = ShoppingCartModel
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if ShoppingCartModel.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Рецепт уже в списке покупок.')
        return data
