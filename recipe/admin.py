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
    list_display = ['name', 'user',]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'user', 'recipe']
    list_select_related = ['recipe']
    search_fields = ['recipe', 'text']
    list_display_links = ['text', 'user']

    def comments_count(self, obj):
        return Comment.objects.filter(recipe=obj.recipe).count()
    comments_count.short_description = 'Total Comment'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe', 'vote_type' , 'upvote_count', 'downvote_count']
    list_display_links = ['user', 'recipe']

    def upvote_count(self, obj):
        return Rating.objects.filter(recipe=obj.recipe, vote_type='upvotes')
    upvote_count.short_description = 'Upvotes'

    def downvote_count(self, obj):
        return Rating.objects.filter(recipe=obj.recipe, vote_type='downvote')
    downvote_count.short_description = 'downvotes'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


