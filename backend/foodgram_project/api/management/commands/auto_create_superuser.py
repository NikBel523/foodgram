import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда для автоматического создания суперюзера."""

    help = 'Автоматическое создание первого суперюзера.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin1@fake.com')
            username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin1')
            first_name = os.getenv('DJANGO_SUPERUSER_FIRST_NAME', 'admin1')
            last_name = os.getenv('DJANGO_SUPERUSER_LAST_NAME', 'admin1')
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'nimda1!Q')
            User.objects.create_superuser(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Суперюзер {username} создан'),
            )
        else:
            self.stdout.write(self.style.SUCCESS('Суперюзер уже есть.'))
