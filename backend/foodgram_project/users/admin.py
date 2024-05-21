from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FoodgramUser, SubscriptionModel


class FoodgramUserAdmin(admin.ModelAdmin):
    """Администратор пользователей."""

    list_display = (
        'username',
        'email',
        'role',
    )

    search_fields = (
        'username',
        'email',
    )


class SubscriptionAdmin(admin.ModelAdmin):
    """Администратор для подписок."""

    list_display = (
        'user',
        'subscription',
    )

    search_fields = ('user',)


admin.site.register(FoodgramUser, UserAdmin)
admin.site.register(SubscriptionModel, SubscriptionAdmin)
