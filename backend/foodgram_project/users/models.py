from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH_150 = 150
ROLE_USER = 'user'
ROLE_ADMIN = 'admin'


class FoodgramUser(AbstractUser):
    """Модель для замены стандартной пользовательской модели."""

    role = models.CharField(max_length=MAX_LENGTH_150,
                            default=ROLE_USER,
                            choices=(
                                (ROLE_USER, 'user'),
                                (ROLE_ADMIN, 'admin'),
                            ))

    avatar = models.ImageField(
        upload_to='images/avatars/',
        null=True,
        default=None
    )

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN or self.is_superuser or self.is_staff

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = ROLE_ADMIN

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
