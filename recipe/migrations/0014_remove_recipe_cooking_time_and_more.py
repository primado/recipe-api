# Generated by Django 4.1 on 2024-05-03 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_alter_recipe_recipe_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='cooking_time',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='time_duration_unit',
        ),
        migrations.AddField(
            model_name='recipe',
            name='cooking_time_duration',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]