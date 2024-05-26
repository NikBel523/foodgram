from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet as DjoserUserViewSet


class FoodgramUserViewSet(DjoserUserViewSet):
    """Класс для внесения изменения в базовый get_permissions."""

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        else:
            return super().get_permissions()

        return [permission() for permission in self.permission_classes]
