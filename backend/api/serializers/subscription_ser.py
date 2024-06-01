from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .users_ser import UserSerializer
from api.serializers.recipes_ser import ShortRecipeInfoSerializer
from users.models import SubscriptionModel


User = get_user_model()


class SubscriptionUserSerializer(UserSerializer):
    """Сериализатор для работы с подписками."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = int(request.query_params.get('recipes_limit', 0))
        recipes_qs = obj.recipes.all()
        if recipes_limit:
            recipes_qs = recipes_qs[:recipes_limit]
        return ShortRecipeInfoSerializer(recipes_qs, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionModel
        fields = ('user', 'subscription')
        validators = [
            UniqueTogetherValidator(
                queryset=SubscriptionModel.objects.all(),
                fields=['user', 'subscription'],
                message='Вы уже подписаны на пользователя'
            )
        ]

    def validate(self, data):
        user = self.context['request'].user
        subscription = data['subscription']

        if user == subscription:
            raise serializers.ValidationError('Нельзя подписаться на себя.')

        return data
