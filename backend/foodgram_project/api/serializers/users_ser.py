from django.contrib.auth import get_user_model
from rest_framework import serializers

from .base64_field import Base64ImageField
from users.models import SubscriptionModel

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SubscriptionModel.objects.filter(
                user=request.user,
                subscription=obj,
            ).exists()
        return False


class AvatarChangeSerializer(serializers.ModelSerializer):

    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)
