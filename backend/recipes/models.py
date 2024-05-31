import random
import string

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

NAME_MAX_LENGTH = 150
SHORT_LINK_LENGTH =10

User = get_user_model()


class TagModel(models.Model):
    """Модель для создания тегов."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Тег',
        unique=True,
    )
    slug = models.SlugField(max_length=16, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class IngredientModel(models.Model):
    """Общая модель ингредиентов."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название ингредиента',
    )

    measurement_unit = models.CharField(
        max_length=16,
        verbose_name='Ед. измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        default_related_name = 'ingredient'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return self.name


class RecipeModel(models.Model):
    """Модель отвечающая за полный рецепт."""

    tags = models.ManyToManyField(TagModel)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )

    ingredients = models.ManyToManyField(
        IngredientModel,
        through='RecipeIngredientsModel',
        blank=False,
    )

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название рецепта',
    )

    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    text = models.TextField(verbose_name='Описание рецепта')

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления, мин.',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Нужно назначить время приготовления.',
            ),
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    short_link = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Короткая ссылка'
    )

    def generate_short_link(self):
        """Генерация короткой ссылки."""
        characters = string.ascii_letters + string.digits
        short_link = ''.join(
            random.choice(characters) for _ in range(SHORT_LINK_LENGTH)
        )
        while RecipeModel.objects.filter(short_link=short_link).exists():
            short_link = ''.join(
                random.choice(characters) for _ in range(SHORT_LINK_LENGTH)
            )
        return short_link

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = self.generate_short_link()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class RecipeIngredientsModel(models.Model):
    """Ингредиенты в составе рецептов."""

    recipe_name = models.ForeignKey(RecipeModel, on_delete=models.CASCADE)
    name = models.ForeignKey(IngredientModel, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Нужно назначить количество ингредиентов.',
            ),
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        default_related_name = 'recipeingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe_name', 'name'],
                name='unique_ingredient_in_recipe',
            ),
        ]

    def __str__(self):
        return f'{self.name} для рецепта {self.recipe_name}'


class BaseRecipeUserModel(models.Model):
    """Базовая модель для связей рецепт-пользователь."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(RecipeModel, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class FavoriteModel(BaseRecipeUserModel):
    """Модель формирующая связи в избранном."""

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'
        default_related_name = 'favorite'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_user_favor',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} добавлен {self.user}'


class ShoppingCartModel(BaseRecipeUserModel):
    """Модель формирующая связи в списке покупок."""

    class Meta:
        verbose_name = 'Рецепт в покупках'
        verbose_name_plural = 'Рецепты в покупках'
        default_related_name = 'shoppingcart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_user_cart',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} добавлен в покупки {self.user}'
