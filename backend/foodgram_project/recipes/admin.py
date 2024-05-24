from django.db.models import Count
from django.contrib import admin

from .models import (IngredientModel, RecipeIngredientsModel, RecipeModel,
                     ShoppingCartModel, TagModel)


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
        'favorite_count',
    )

    list_filter = ('tags',)
    search_fields = ('name', 'author',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(fav_count=Count('favoritemodel'))
        return queryset

    def favorite_count(self, obj):
        return obj.fav_count

    favorite_count.short_description = 'Кол-во добавлений в избранное'


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
    )

    list_filter = ('recipe_name', 'name')


class ShoppingCartModelAdmin(admin.ModelAdmin):
    """Администратор для связей пользователей и реуептов в корзине."""

    list_display = (
        'user',
        'recipe',
    )

    search_fields = ('user',)


admin.site.register(TagModel, TagAdmin)
admin.site.register(RecipeModel, RecipeAdmin)
admin.site.register(IngredientModel, IngredientAdmin)
admin.site.register(ShoppingCartModel, ShoppingCartModelAdmin)
admin.site.register(RecipeIngredientsModel, RecipeIngredientsAdmin)
