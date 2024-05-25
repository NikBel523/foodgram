from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .base64_field import Base64ImageField
from .users_ser import UserSerializer
from recipes.models import (IngredientModel, FavoriteModel,
                            RecipeIngredientsModel,
                            RecipeModel, TagModel, ShoppingCartModel)


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


class RecipeReadSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return FavoriteModel.objects.filter(
            user=request.user,
            recipe=obj,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return False

    def get_ingredients(self, obj):
        ingredients = RecipeIngredientsModel.objects.filter(recipe_name=obj)
        return RecipeIngredientsSerializer(ingredients, many=True).data


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализавтор для записи и апдейта рецептов."""

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

    def validate(self, data):
        required_fields = [
            'tags', 'ingredients', 'image', 'name', 'text', 'cooking_time',
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(
                    {field:
                        f'Поле {field} обязательноедля создания рецепта.'},
                )
        return data

    def validate_tags(self, value):
        if len(value) != len(set(value)):
            raise ValidationError({'tags': 'Теги не могут повторяться.'})
        return value

    def validate_ingredients(self, value):
        if len(value) != len(set(value)):
            raise ValidationError({'ingredients': 'Нужны разные ингредиенты.'})
        for ingredient in value:
            if ingredient['amount'] < 1:
                raise ValidationError({'ingredients': 'Кол-во не меньше 1.'})
        return value

    def validate_cooking_time(self, value):
        if value < 1:
            raise ValidationError({'cooking_time': 'Время не меньше 1.'})
        return value

    def to_representation(self, instance):
        return RecipeReadSerializer(instance).data

    def _create_or_update_ingredients(self, recipe, ingredients_data):
        for ingredient_data in ingredients_data:
            RecipeIngredientsModel.objects.create(
                recipe_name=recipe,
                name=ingredient_data.pop('name')['id'],
                **ingredient_data,
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = RecipeModel.objects.create(**validated_data)
        recipe.tags.set(tags)

        self._create_or_update_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
        )
        instance.save()

        instance.ingredients.clear()
        self._create_or_update_ingredients(instance, ingredients)

        instance.tags.clear()
        instance.tags.set(tags)

        return instance


class FavoritedSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeModel
        fields = ('id', 'name', 'image', 'cooking_time')
