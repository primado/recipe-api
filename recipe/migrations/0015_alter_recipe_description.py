# Generated by Django 4.1 on 2024-05-06 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0014_remove_recipe_cooking_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
