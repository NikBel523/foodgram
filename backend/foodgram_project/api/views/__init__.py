from .ingredients_v import IngredientViewSet
from .recipes_v import RecipeViewSet, TagViewSet
from .avatar_v import AvatarChangeView

__all__ = [
    AvatarChangeView,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
]
