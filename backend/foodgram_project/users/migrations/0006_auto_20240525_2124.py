# Generated by Django 3.2.16 on 2024-05-25 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20240521_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodgramuser',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]
