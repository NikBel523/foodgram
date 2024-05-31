from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import FoodgramUser, SubscriptionModel


@admin.register(FoodgramUser)
class FoodgramUserAdmin(UserAdmin):
    """Администратор пользователей."""

    list_display = (
        'username',
        'email',
    )

    search_fields = (
        'username',
        'email',
    )


@admin.register(SubscriptionModel)
class SubscriptionAdmin(admin.ModelAdmin):
    """Администратор для подписок."""

    list_display = (
        'user',
        'subscription',
    )

    search_fields = ('user',)


admin.site.unregister(Group)
