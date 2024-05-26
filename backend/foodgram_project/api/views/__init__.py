from .avatar_v import AvatarChangeView
from .ingredients_v import IngredientViewSet
from .recipes_v import AddFavoriteView, RecipeViewSet, TagViewSet
from .shopping_cart_v import DownloadShoppingCartView, ManageShoppingCartView
from .subscription_v import SubscribeView, SubscriptionListView
from .users_v import FoodgramUserViewSet

__all__ = [
    AddFavoriteView,
    AvatarChangeView,
    DownloadShoppingCartView,
    IngredientViewSet,
    RecipeViewSet,
    SubscribeView,
    SubscriptionListView,
    ManageShoppingCartView,
    TagViewSet,
    FoodgramUserViewSet,
]
