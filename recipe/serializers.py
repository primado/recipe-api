from rest_framework import serializers
from .models import *
from accounts.serializers import CustomUserSerializers


# Create your serializers here

class RecipeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCollectionRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = RecipeCollectionRecipe
        fields = ['recipe', 'collection', 'is_bookmarked']


class RecipeReadSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class CreatCollectionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)

    class Meta:
        model = RecipeCollection
        fields = ['name', 'description', 'visibility', 'user']


class RecipeCollectionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    collection_recipes = RecipeCollectionRecipeSerializer(many=True, source='recipecollectionrecipe_set')

    class Meta:
        model = RecipeCollection
        fields = ['id', 'name', 'description', 'user', 'visibility', 'collection_recipes', 'created_at', 'last_updated']

    def create(self, validated_data):
        recipes_data = validated_data.pop('recipecollectionrecipe_set')
        collection = RecipeCollection.objects.create(**validated_data)
        for recipe_data in recipes_data:
            RecipeCollectionRecipe.objects.create(collection=collection, **recipe_data)
        return collection

    def update(self, instance, validated_data):
        recipes_data = validated_data.pop('recipecollectionrecipe_set')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        for recipe_data in recipes_data:
            recipe_instance = RecipeCollectionRecipe.objects.get(collection=instance, recipe=recipe_data['recipe'])
            recipe_instance.is_bookmarked = recipe_data.get('is_bookmarked', recipe_instance.is_bookmarked)
            recipe_instance.save()

        return instance


# class RetrieveCollectionsRecipesSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializers(read_only=True)
#     class Meta:
#         class Meta:
#             model =
#             fields = '__all__'


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
