from django.contrib.auth import get_user_model
from rest_framework import serializers

from .users_ser import UserSerializer
from api.serializers.recipes_ser import FavoritedSerializer


User = get_user_model()


class SubscriptionUserSerializer(UserSerializer):
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
        return FavoritedSerializer(recipes_qs, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
