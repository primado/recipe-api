# Generated by Django 4.1 on 2024-03-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_rating_parent_comment_alter_commentvote_vote_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='parent_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ManyToManyField(blank=True, null=True, to='recipe.comment'),
        ),
    ]
