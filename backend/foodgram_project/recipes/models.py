from django.contrib.auth import get_user_model
from django.db import models

NAME_MAX_LENGTH = 150

User = get_user_model()


class TagModel(models.Model):
    """Модель для создания тегов."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Тег',
        unique=True,
    )
    slug = models.SlugField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('slug',)


class IngredientModel(models.Model):
    """Общая модель ингридиентов."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название ингридиента',
    )

    units = models.CharField(max_length=16)  # choices=UNITS ?

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class RecipeModel(models.Model):
    """Модель отвечающая за полный рецепт."""

    # TODO пересмотреть on_delete
    tags = models.ForeignKey(TagModel, on_delete=models.CASCADE)

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

    # TODO is_favorited & is_in_shopping_cart ?

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

    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления, мин.',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('created_at',)


class RecipeIngredientsModel(models.Model):
    """Ингридиенты в составе рецептов."""

    recipe_name = models.ForeignKey(RecipeModel, on_delete=models.CASCADE)
    # TODO пересмотреть on_delete
    name = models.ForeignKey(IngredientModel, on_delete=models.CASCADE)

    measurement_unit = models.CharField(max_length=16)  # choices=UNITS ?

    amount = models.SmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.name} для рецпета {self.recipe_name}'

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'
