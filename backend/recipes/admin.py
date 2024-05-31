from django.db.models import Count
from django.contrib import admin

from .models import (IngredientModel, RecipeIngredientsModel, RecipeModel,
                     ShoppingCartModel, TagModel, FavoriteModel)


class IngredientsInline(admin.TabularInline):
    """Инлайн для ингредиентов в админ-панели рецептов."""

    model = RecipeModel.ingredients.through


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    """Администратор для тегов."""

    list_display = (
        'name',
        'slug',
    )

    search_fields = ('name',)


@admin.register(RecipeModel)
class RecipeAdmin(admin.ModelAdmin):
    """Администратор для рецептов."""

    inlines = [IngredientsInline]

    list_display = (
        'name',
        'author',
        'cooking_time',
        'created_at',
        'favorite_count',
    )

    list_filter = ('tags',)
    search_fields = ('name', 'author',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(fav_count=Count('favorite'))
        return queryset

    @admin.display(description='Кол-во добавлений в избранное')
    def favorite_count(self, obj):
        return obj.fav_count


@admin.register(IngredientModel)
class IngredientAdmin(admin.ModelAdmin):
    """Администратор для отдельных ингредиентов."""

    list_display = (
        'name',
        'measurement_unit',
    )

    search_fields = ('name',)


@admin.register(RecipeIngredientsModel)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    """Администратор для ингредиентов в составе рецептов."""

    list_display = (
        'recipe_name',
        'name',
        'amount',
    )

    list_filter = ('recipe_name', 'name')


@admin.register(FavoriteModel, ShoppingCartModel)
class UserRecipeLinkAdmin(admin.ModelAdmin):
    """Администратор для избранного и списка покупок."""

    list_display = (
        'user',
        'recipe',
    )

    search_fields = ('user',)
