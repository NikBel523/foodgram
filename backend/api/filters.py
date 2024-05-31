from django_filters import rest_framework as filters

from recipes.models import IngredientModel, RecipeModel, TagModel


class RecipeFilter(filters.FilterSet):
    """Основной фильтр для сортировки по тегам, избранному, списку покупок."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=TagModel.objects.all(),
        label='Теги'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',
        label='В избраном',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        label='В спсике покупок',
    )

    class Meta:
        model = RecipeModel
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shoppingcart__user=user)
        return queryset


class IngredientFilter(filters.FilterSet):
    """Дополнительный фильтр для названия ингредиентов."""

    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = IngredientModel
        fields = ['name']
