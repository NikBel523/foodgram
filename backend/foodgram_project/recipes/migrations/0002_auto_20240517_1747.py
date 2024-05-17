# Generated by Django 3.2.16 on 2024-05-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipemodel',
            name='tags',
        ),
        migrations.AddField(
            model_name='recipemodel',
            name='tags',
            field=models.ManyToManyField(to='recipes.TagModel'),
        ),
    ]