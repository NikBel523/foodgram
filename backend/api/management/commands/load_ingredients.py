import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from recipes.models import IngredientModel


class Command(BaseCommand):
    """Команда загрузки ингредиентов."""

    help = 'Загружает ингредиенты из CSV файла.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Путь к CSV файлу',
            default=os.path.join(settings.BASE_DIR, 'data', 'ingredients.csv')
        )

    def handle(self, *args, **options):
        file_path = options['file']

        if not os.path.exists(file_path):
            raise CommandError(f'Файл {file_path} не существует.')

        ingredients = []

        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    name, measurement_unit = row
                    ingredient = IngredientModel(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
                    ingredients.append(ingredient)

            # Проверка уникальности ингредиентов
            existing_ingredients = set(
                IngredientModel.objects.values_list('name', 'measurement_unit')
            )
            new_ingredients = [
                ingredient for ingredient in ingredients
                if (
                    (ingredient.name, ingredient.measurement_unit)
                    not in existing_ingredients
                )
            ]

            IngredientModel.objects.bulk_create(new_ingredients)
            self.stdout.write(self.style.SUCCESS('Ингредиенты загружены.'))
        except Exception as e:
            raise CommandError(f'Что-то пошло не по плану: {e}')
