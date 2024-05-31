from .ingredients_v import IngredientViewSet
from .recipes_v import RecipeViewSet, TagViewSet
from .users_v import FoodgramUserViewSet

__all__ = [
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    FoodgramUserViewSet,
]
