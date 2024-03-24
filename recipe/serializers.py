from rest_framework import serializers
from .models import *


# Create your serializers here

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCollection
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RecipeVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__a__'


class RecipeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
