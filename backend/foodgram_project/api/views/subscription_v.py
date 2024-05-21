from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import SubscriptionUserSerializer
from users.models import SubscriptionModel

User = get_user_model()

TEXT_ERROR_404 = 'Пользователь не найден.'


class SubscriptionListView(generics.ListAPIView):

    serializer_class = SubscriptionUserSerializer

    def get_queryset(self):
        return User.objects.filter(subscription__user=self.request.user)


class SubscribeView(APIView):

    def post(self, request, id):
        user = request.user

        try:
            subscription = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {'errors': TEXT_ERROR_404},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user == subscription:
            return Response(
                {'errors': 'нельзя подписаться на себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription, created = SubscriptionModel.objects.get_or_create(
            user=user,
            subscription=subscription,
        )

        if not created:
            return Response(
                {'errors': 'Подписка уже существует.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SubscriptionUserSerializer(
            subscription.subscription,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        try:
            subscription = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {'errors': TEXT_ERROR_404},
                status=status.HTTP_404_NOT_FOUND,
            )

        subscription_instance = SubscriptionModel.objects.filter(
            user=user,
            subscription=subscription,
        ).first()
        if subscription_instance:
            subscription_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': 'Нет подписки на пользователя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
