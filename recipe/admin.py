from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'description', 'difficulty_level', 'visibility']
    search_fields = ['description', 'ingredient']
    list_display_links = ['title', 'user']


@admin.register(RecipeCollection)
class RecipeCollection(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'description']


@admin.register(RecipeCollectionRecipe)
class RecipeCollectionRecipe(admin.ModelAdmin):
    list_display = ['recipe_id', 'recipe', 'collection', 'recipe_user']
    list_display_links = ['recipe', 'collection']

    def recipe_user(self, obj):
        return obj.recipe.user

    recipe_user.shor_description = 'Recipe User'

    def recipe_id(self, obj):
        return obj.recipe.id

    recipe_id.short_description = 'Recipe ID'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text', 'recipe']
    list_select_related = ['recipe']
    search_fields = ['recipe', 'text']
    list_display_links = ['text', 'user']

    def comments_count(self, obj):
        return Comment.objects.filter(recipe=obj.recipe).count()

    comments_count.short_description = 'Total Comment'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe', 'vote_type', 'upvote_count', 'downvote_count']
    list_display_links = ['user', 'recipe']

    def upvote_count(self, obj):
        return Rating.objects.filter(recipe=obj.recipe, vote_type='upvote').count()

    upvote_count.short_description = 'Upvote'

    def downvote_count(self, obj):
        return Rating.objects.filter(recipe=obj.recipe, vote_type='downvote').count()

    downvote_count.short_description = 'Downvote'


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment', ]
    list_display_links = ['user', 'comment']

    def upvote_count(self, obj):
        return CommentVote.objects.filter(comment=obj.comment, vote_type='upvote').count()

    upvote_count.short_description = 'Upvote Count'

    def downvote_count(self, obj):
        return CommentVote.objects.filter(comment=obj.comment, vote_type='downvote').count()

    downvote_count.short_description = 'Downvote count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
