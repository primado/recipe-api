# Generated by Django 4.1 on 2024-04-03 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_recipe_time_choice_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time_choice',
            new_name='time_duration_unit',
        ),
    ]
