from django_filters import rest_framework as filters
from django.db.models import Exists, OuterRef
from recipes.models import RecipeModel, FavoriteModel, ShoppingCartModel


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug', lookup_expr='icontains')
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
        print(value)
        if value:
            return queryset.filter(
                Exists(
                    FavoriteModel.objects.filter(
                        user=self.request.user,
                        recipe=OuterRef('id'),
                    )
                )
            )
        return queryset.exclude(
            Exists(
                FavoriteModel.objects.filter(
                    user=self.request.user,
                    recipe=OuterRef('id'),
                )
            )
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        print(value)
        if value:
            return queryset.filter(
                Exists(
                    ShoppingCartModel.objects.filter(
                        user=self.request.user,
                        recipe=OuterRef('id'),
                    )
                )
            )
        return queryset.exclude(
            Exists(
                ShoppingCartModel.objects.filter(
                    user=self.request.user,
                    recipe=OuterRef('id'),
                )
            )
        )
