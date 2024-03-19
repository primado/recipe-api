from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_id', 'description', 'difficulty_level', 'visibility']
    search_fields = ['description', 'ingredient']

@admin.register(RecipeCollection)
class RecipeCollection(admin.ModelAdmin):
    list_display = ['name', 'user_id',]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'user_id', 'recipe_id']
    list_select_related = ['recipe_id']
    search_fields = ['recipe_id', 'text']
    list_display_links = ['text', 'user_id']

    def comments_count(self, obj):
        return Comment.objects.filter(recipe=obj.recipe).count()
    comments_count.short_description = 'Total Comment'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'recipe_id', 'upvotes_count', 'downvotes_count']
    list_display_links = ['user_id', 'recipe_id']

    def upvotes_count(self, obj):
        number = Rating.objects.filter(recipe=obj.recipe, upvote=True).count()
        return number
    upvotes_count.short_descritioon = 'Upvotes'

    def downvotes_count(self, obj):
        return Rating.objects.filter(recipe=obj.recipe, downvote=True).count()
    downvotes_count.short_description = 'Downvotes'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


