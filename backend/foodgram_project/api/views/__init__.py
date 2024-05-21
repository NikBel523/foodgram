from .ingredients_v import IngredientViewSet
from .recipes_v import AddFavoriteView, RecipeViewSet, TagViewSet
from .avatar_v import AvatarChangeView

__all__ = [
    AddFavoriteView,
    AvatarChangeView,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
]
