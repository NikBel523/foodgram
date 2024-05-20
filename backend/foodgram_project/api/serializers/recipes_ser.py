from rest_framework import serializers

from recipes.models import RecipeIngredientsModel, RecipeModel, TagModel
from .base64_field import Base64ImageField
from .users_ser import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'slug',)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для данных из модели RecipeIngredientsModel."""

    name = serializers.ReadOnlyField(source='name.name')
    measurement_unit = serializers.ReadOnlyField(
        source='name.measurement_unit',
    )

    class Meta:
        model = RecipeIngredientsModel
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для данных к рецептам."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

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

    def get_ingredients(self, obj):
        ingredients = RecipeIngredientsModel.objects.filter(recipe_name=obj)
        return RecipeIngredientsSerializer(ingredients, many=True).data
