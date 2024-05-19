from django.contrib import admin

from .models import (IngredientModel, RecipeIngredientsModel, RecipeModel,
                     TagModel)


class IngredientsInline(admin.TabularInline):
    """Инлайн для ингредиентов в админ-панели рецептов."""

    model = RecipeModel.ingredients.through


class TagAdmin(admin.ModelAdmin):
    """Администратор для тегов."""

    list_display = (
        'name',
        'slug',
    )

    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    """Администратор для рецептов."""

    inlines = [IngredientsInline]

    list_display = (
        'name',
        'author',
        'cooking_time',
        'created_at',
    )

    list_filter = ('tags',)
    search_fields = ('name', 'author',)


class IngredientAdmin(admin.ModelAdmin):
    """Администратор для отдельных ингредиентов."""

    list_display = (
        'name',
        'measurement_unit',
    )

    search_fields = ('name',)


class RecipeIngredientsAdmin(admin.ModelAdmin):
    """Администратор для ингредиентов в составе рецептов."""

    list_display = (
        'recipe_name',
        'name',
        'amount',
        # 'measurement_unit',
    )

    list_filter = ('recipe_name', 'name')


admin.site.register(TagModel, TagAdmin)
admin.site.register(RecipeModel, RecipeAdmin)
admin.site.register(IngredientModel, IngredientAdmin)
admin.site.register(RecipeIngredientsModel, RecipeIngredientsAdmin)
