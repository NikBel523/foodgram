from rest_framework import serializers

from recipes.models import TagModel, RecipeIngredientsModel, RecipeModel
from .users_ser import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'slug',)


class RecipeIngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredientsModel
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(read_only=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = RecipeModel
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False
