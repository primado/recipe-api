# Generated by Django 4.2 on 2024-03-20 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_image',
            field=models.ImageField(blank=True, null=True, upload_to='recipe-images'),
        ),
    ]