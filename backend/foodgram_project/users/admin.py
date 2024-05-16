from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FoodgramUser


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


admin.site.register(FoodgramUser, UserAdmin)
