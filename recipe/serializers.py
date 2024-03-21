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


