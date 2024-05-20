from rest_framework import serializers

from .base64_field import Base64ImageField
from .users_ser import UserSerializer
from recipes.models import (IngredientModel, RecipeIngredientsModel,
                            RecipeModel, TagModel)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'slug',)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для данных из модели RecipeIngredientsModel."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=IngredientModel.objects.all(), source='name.id'
    )
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


class RecipeWriteSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(
        queryset=TagModel.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientsSerializer(many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = RecipeModel
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):

        return RecipeSerializer(instance).data

    def _create_or_update_ingredients(self, recipe, ingredients_data):
        for ingredient_data in ingredients_data:
            ingredient = ingredient_data.pop('name')['id']
            RecipeIngredientsModel.objects.create(
                recipe_name=recipe,
                name=ingredient,
                **ingredient_data,
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = RecipeModel.objects.create(**validated_data)
        recipe.tags.set(tags)

        self._create_or_update_ingredients(recipe, ingredients_data)
        return recipe
