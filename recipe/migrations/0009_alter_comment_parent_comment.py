# Generated by Django 4.1 on 2024-03-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_remove_rating_parent_comment_comment_parent_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ManyToManyField(blank=True, to='recipe.comment'),
        ),
    ]