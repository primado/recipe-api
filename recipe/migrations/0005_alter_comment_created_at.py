# Generated by Django 4.1 on 2024-03-23 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_commentvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TimeField(auto_now=True),
        ),
    ]
