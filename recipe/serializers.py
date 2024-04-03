from rest_framework import serializers
from accounts.serializers import CustomUserSerializers
from .models import *



# Create your serializers here

class RecipeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    class Meta:
        model = Recipe
        fields = ['']



class RecipeCollectionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    class Meta:
        model = RecipeCollection
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'


class RecipeVoteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    class Meta:
        model = Rating
        fields = '__a__'


class RecipeRatingSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    class Meta:
        model = Rating
        fields = '__all__'


class CommentVoteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    class Meta:
        model = CommentVote
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
