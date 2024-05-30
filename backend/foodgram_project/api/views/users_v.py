from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import AvatarChangeSerializer

User = get_user_model()


class FoodgramUserViewSet(DjoserUserViewSet):
    """Класс для внесения изменения в базовый get_permissions."""

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        else:
            return super().get_permissions()

        return [permission() for permission in self.permission_classes]

    @action(methods=['put'], detail=False, url_path='me/avatar')
    def avatar(self, request):
        """Добавление аватара"""
        serializer = self._set_avatar(request.data)
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        """Удаление аватара"""
        self._set_avatar(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _set_avatar(self, data):
        instance = self.get_instance()
        serializer = AvatarChangeSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer
