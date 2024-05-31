from rest_framework import serializers

from recipes.models import FavoriteModel


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов в избранное."""

    class Meta:
        model = FavoriteModel
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if FavoriteModel.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Рецепт уже в избранном.')
        return data
