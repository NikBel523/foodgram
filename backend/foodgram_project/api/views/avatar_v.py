from django.contrib.auth import get_user_model
from rest_framework import generics, mixins

from api.serializers import AvatarChangeSerializer

User = get_user_model()


class AvatarChangeView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AvatarChangeSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.avatar.delete()
        instance.avatar = None
        instance.save()
