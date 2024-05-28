from django_filters import rest_framework as filters

from recipes.models import IngredientModel, RecipeModel


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(method='filter_tags', label='Теги')
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

    def filter_tags(self, queryset, name, value):
        tags = self.request.GET.getlist('tags')
        return queryset.filter(tags__slug__in=tags).distinct()

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(is_favorited__gt=0)
        return queryset.filter(is_favorited=0)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(is_in_shopping_cart__gt=0)
        return queryset.filter(is_in_shopping_cart=0)


class IngredientFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = IngredientModel
        fields = ['name']
