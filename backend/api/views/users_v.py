from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.paginator import LimitPageNumberPagination
from api.serializers import (
    AvatarChangeSerializer,
    SubscriptionManageSerializer,
    SubscriptionUserSerializer,
)
from users.models import SubscriptionModel

User = get_user_model()


class FoodgramUserViewSet(DjoserUserViewSet):
    """Класс для внесения изменения в базовый get_permissions."""

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        else:
            return super().get_permissions()

        return [permission() for permission in self.permission_classes]

    # actions для работы с аватарами
    @action(methods=['put'], detail=False, url_path='me/avatar')
    def avatar(self, request):
        """Добавление аватара."""
        serializer = self._set_avatar(request.data)
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        """Удаление аватара."""
        instance = self.get_instance()
        instance.avatar.delete()
        instance.avatar = None
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _set_avatar(self, data):
        instance = self.get_instance()
        serializer = AvatarChangeSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    # actions для работы с подписками
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions',
    )
    def subscriptions(self, request):
        """Получение списка подписок текущего пользователя."""
        user = request.user
        queryset = User.objects.filter(subscription__user=user)
        paginator = LimitPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = SubscriptionUserSerializer(
            paginated_queryset,
            many=True,
            context={'request': request},
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='subscribe',
    )
    def subscription(self, request, id):
        """Подписка на пользователя."""
        subscription = get_object_or_404(User, id=id)
        return self._create_subscription(request, subscription)

    @subscription.mapping.delete
    def delete_subscription(self, request, id):
        """Отмена подписки на пользователя."""
        subscription = get_object_or_404(User, id=id)
        return self._delete_subscription(request, subscription)

    def _create_subscription(self, request, subscription):
        """Создание подписки на пользователя."""
        serializer = SubscriptionManageSerializer(
            data={'user': request.user.id, 'subscription': subscription.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            SubscriptionUserSerializer(
                subscription,
                context={'request': request},
            ).data,
            status=status.HTTP_201_CREATED
        )

    def _delete_subscription(self, request, subscription):
        """Удаление подписки на пользователя."""
        user = request.user
        subscription_instance = SubscriptionModel.objects.filter(
            user=user,
            subscription=subscription,
        ).delete()

        if subscription_instance[0]:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Нет подписки на пользователя.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
