from rest_framework import generics

from api.serializers import AvatarChangeSerializer


class AvatarChangeView(generics.RetrieveUpdateDestroyAPIView):
    """Вью для обновления и удаления аватаров пользователей."""

    serializer_class = AvatarChangeSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.avatar.delete()
        instance.avatar = None
        instance.save()
