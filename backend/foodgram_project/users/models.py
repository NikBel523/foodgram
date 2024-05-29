from django.contrib.auth import validators
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q

MAX_LENGTH_150 = 150
ROLE_USER = 'user'
ROLE_ADMIN = 'admin'


class FoodgramUser(AbstractUser):
    """Модель для замены стандартной пользовательской модели."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Используется в api.permissions.IsAuthorOrAdminOrReadOnly
    role = models.CharField(
        max_length=MAX_LENGTH_150,
        default=ROLE_USER,
        choices=(
            (ROLE_USER, 'user'),
            (ROLE_ADMIN, 'admin'),
        )
    )

    avatar = models.ImageField(
        upload_to='images/avatars/',
        null=True,
        default=None
    )

    username = models.CharField(
        max_length=MAX_LENGTH_150,
        unique=True,
        validators=[validators.UnicodeUsernameValidator()],
    )
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=MAX_LENGTH_150)
    last_name = models.CharField(max_length=MAX_LENGTH_150)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN or self.is_superuser or self.is_staff

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = ROLE_ADMIN

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class SubscriptionModel(models.Model):
    """Модель хранения информации о подписках пользователей."""

    user = models.ForeignKey(
        FoodgramUser, on_delete=models.CASCADE, related_name='follower'
    )

    subscription = models.ForeignKey(
        FoodgramUser, on_delete=models.CASCADE, related_name='subscription'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscription'],
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~Q(subscription__exact=F('user')),
                name='cant_follow_yourself',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.user} на {self.subscription}'
