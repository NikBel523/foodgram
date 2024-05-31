# Generated by Django 3.2.16 on 2024-05-25 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_auto_20240522_1346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritemodel',
            options={'default_related_name': 'favorite', 'verbose_name': 'Рецепт в избранном', 'verbose_name_plural': 'Рецепты в избранном'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcartmodel',
            options={'default_related_name': 'shoppingcart', 'verbose_name': 'Рецепт в покупках', 'verbose_name_plural': 'Рецепты в покупках'},
        ),
        migrations.AlterField(
            model_name='favoritemodel',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipes.recipemodel'),
        ),
        migrations.AlterField(
            model_name='favoritemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shoppingcartmodel',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcart', to='recipes.recipemodel'),
        ),
        migrations.AlterField(
            model_name='shoppingcartmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcart', to=settings.AUTH_USER_MODEL),
        ),
    ]