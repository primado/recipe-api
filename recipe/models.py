from django.db import models
from accounts.models import CustomUser


# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    ingredient = models.TextField(blank=True)
    instruction = models.TextField(blank=True)
    cooking_time = models.IntegerField(blank=True)

    DIFFICULTY_LEVEL_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    PRIVATE = "private"
    PUBLIC = "public"
    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private")
    ]

    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)
    difficulty_level = models.CharField(max_length=7, choices=DIFFICULTY_LEVEL_CHOICES)
    recipe_image = models.ImageField(upload_to='recipe-images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Recipe'
        managed = True
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'
        ordering = ['-last_updated']


class RecipeCollection(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ManyToManyField(Recipe, through="RecipeCollectionRecipe", related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'RecipeCollection'
        managed = True
        verbose_name = 'recipe collection'
        verbose_name_plural = 'recipe collections'
        ordering = ['-created_at']


class RecipeCollectionRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    collection = models.ForeignKey(RecipeCollection, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'Comment'
        managed = True
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['-created_at']


class Rating(models.Model):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'
    VOTE_CHOICE = [
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote")
    ]
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICE, blank=True, null=True)

    class Meta:
        unique_together = [['user_id', 'recipe_id']]

class CommentVote(models.Model):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'
    VOTE_CHOICE = [
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICE)

    class Meta:
        db_table = 'CommentVote'
        unique_together = [['user', 'comment']]


class Tag(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Tag'
        managed = True,
        verbose_name = "tag"
        verbose_name_plural = "tag"
        ordering = ['-created_at']
