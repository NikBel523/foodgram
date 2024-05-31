from django.core.management.base import BaseCommand

from recipes.models import TagModel


class Command(BaseCommand):
    """Команда для автоматического создания базовых тегов."""

    help = 'Автоматическое создание тегов bre, din, sup.'

    def handle(self, *args, **kwargs):
        tags = {
            'bre': 'Завтрак',
            'din': 'Обед',
            'sup': 'Ужин',
        }

        tags_to_create = []
        for slug, name in tags.items():
            if not TagModel.objects.filter(slug=slug).exists():
                tags_to_create.append(
                    TagModel(
                        name=name,
                        slug=slug,
                    )
                )

        TagModel.objects.bulk_create(tags_to_create)
        self.stdout.write(
            self.style.SUCCESS(f'Созданы теги {tags_to_create}.'),
        )
