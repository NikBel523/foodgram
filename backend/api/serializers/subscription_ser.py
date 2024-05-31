from django.contrib.auth import get_user_model
from rest_framework import serializers

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
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context['request'].user
        subscription = data['subscription']

        if user == subscription:
            raise serializers.ValidationError('Нельзя подписаться на себя.')

        if SubscriptionModel.objects.filter(
            user=user,
            subscription=subscription,
        ).exists():
            raise serializers.ValidationError('Подписка уже существует.')

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
