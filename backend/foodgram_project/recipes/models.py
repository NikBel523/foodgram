from django.db import models

NAME_MAX_LENGTH = 150


class TagModel(models.Model):
    """Модель для создания тегов."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Тег',
        unique=True,
    )
    slug = models.SlugField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('slug',)
