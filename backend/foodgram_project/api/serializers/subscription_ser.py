from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.serializers.recipes_ser import FavoritedSerializer
from .users_ser import UserSerializer

User = get_user_model()


class SubscriptionUserSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        return FavoritedSerializer(obj.recipes.all(), many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
