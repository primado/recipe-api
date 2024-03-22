from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import *

# Create your views here.

# Recipe CRUD View
class RecipeView(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def get_object(self, recipe_id, user):
        recipe_id =self.kwargs.get('pk')
        user = self.request.user
        try: 
            return self.queryset.get(id=recipe_id, user=user)
        except Recipe.DoesNotExist:
            return None

    def list(self, request):
        user = request.user
        queryset = self.queryset.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Request successful', 'data': serializer.data}, status=status.HTTP_200_OK)



    def create(self, request):

        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'ingredient': request.data.get('ingredient'),
            'intruction': request.data.get('instruction'),
            'cooking_time': request.data.get('cooking_time'),
            'visibility': request.data.get('visibility'),
            'difficulty_level': request.data.get('difficulty_level'),
            'recipe_image': request.data.get('recipe_image'),
            'user': request.user.id
        }

        serializer = self.get_serializer(data=data)
    
        if serializer.is_valid():
            if request.user.id == data['user']:
                serializer.save()
                return Response({'message': 'Recipe created successfully', 'data': serializer.data},  status=status.HTTP_201_CREATED)
            return Response({'message': 'User Unauthorized'}, content_type='multipart/form-data', status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, pk=None, *args, **kwargs):
        recipe_instance = self.get_object(pk, request.user.id)

        if not recipe_instance:
            return Response({'message': 'Recipe does doest not exist'},  status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'ingredient': request.data.get('ingredient'),
            'intruction': request.data.get('instruction'),
            'cooking_time': request.data.get('cooking_time'),
            'visibility': request.data.get('visibility'),
            'difficulty_level': request.data.get('difficulty_level'),
            'recipe_image': request.data.get('recipe_image'),
            'user': request.user.id
        }

        serializer = self.get_serializer(instance=recipe_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Recipe updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def destroy(self, request, pk=None, *args, **kwargs):
        recipe_instance = self.get_object(pk, request.user.id)

        if not recipe_instance:
            return Response({"message": 'Recipe does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        recipe_instance.delete()
        return Response({"messsage": 'Recipe deleted'}, status=status.HTTP_204_NO_CONTENT)
    

# Show Public Recipes to all users
class RecipeFeedView(APIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        visibility = 'public'
        queryset = self.queryset.filter(visibility=visibility)
        if not queryset.exists():
            return Response({'message': 'There are no public recipes'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(queryset, many=True)
        return Response({'message': 'Public recipes', 'data': serializer.data}, status=status.HTTP_200_OK )
    
   

# show private recipes to Recipes author/user
class UserPrivateRecipes(GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(detail=False, methods=['get'])
    def user_private_recipes(self, request):
        visibility = 'private'
        queryset = self.queryset.filter(visibility=visibility, user=request.user)
        if not queryset.exists():
            return Response({'message': 'There are no private recipes for you.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        return Response({'message': 'Your private recipes', 'data': serializer.data}, status=status.HTTP_200_OK)



class RecipeCollectionView(ModelViewSet):
    queryset = RecipeCollection.objects.all()
    serializer_class = RecipeCollectionSerializer
    parser_classes = [MultiPartParser, FormParser]


    def get_object(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except RecipeCollection.DoesNotExist:
            return None


    def list(self, request):
        user = request.user
        queryset = self.queryset.filter(user=user)
        if not self.queryset.exists():
            return Response({'message': 'Recipe collection empty.'}, status=status.HTTP_404_NOT_FOUND)
        
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Request successful', 'data': serializer.data}, status=status.HTTP_200_OK)
    

    def create(self, request):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'user': request.user.id
        }

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            if request.user.id == data['user']:
                serializer.save()
                return Response({'message': 'Recipe collection created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'message': 'User Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, pk, *args, **kwargs):
        collection_instance = self.get_object(pk)
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'user': request.user.id
        }

        if not collection_instance:
            return Response({'message': 'Recipe Collection does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(collection_instance, data=data)
        if serializer.is_valid():
            if request.user.id == data['user']:
                serializer.save()
                return Response({'message': 'Recipe collection updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'User unathorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk, *args, **kwargs):
        collection_instance = self.get_object(pk)
        if not collection_instance:
            return Response({'message': 'Recipe Collection does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        user_id_from_request =collection_instance.user.id
        if request.user.id != user_id_from_request:
            return Response({'message': 'User unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        collection_instance.delete()
        return Response({'message': 'Recipe collection deleted'}, status=status.HTTP_204_NO_CONTENT)


    ### Views for adding and deleting a recipe to and from collection upon a request


    def add_recipe(self, request, pk, *args, **kwargs):
        collection_pk = pk
        try:
            collection = self.queryset.get(pk=collection_pk, user=request.user)
        except RecipeCollection.DoesNotExist:
            return Response({'message': 'Recipe Collection does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'ingredient': request.data.get('ingredient'),
            'instruction': request.data.get('instruction'),
            'cooking_time': request.data.get('cooking_time'),
            'visibility': request.data.get('visibility'),
            'difficulty_level': request.data.get('difficulty_level'),
            'recipe_image': request.data.get('recipe_image'),
            'user': request.user.id
        }
        
        recipe_data = data
        if not recipe_data:
            return Response({'message': 'Recipe data is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        recipe_serializer = RecipeSerializer(data=recipe_data)
        if recipe_serializer.is_valid():
            recipe_serializer.save()
        else: 
            return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        collection.recipe.add(recipe_serializer.instance)
        return Response({'message': 'Recipe added to collection successfully.', 'data': recipe_serializer.data}, status=status.HTTP_200_OK)
    

    def remove_recipe(self, request, *args, **kwargs):
        collection_pk = kwargs.get('pk')
        recipe_pk = self.kwargs.get('recipe_pk')
        try:
            collection = self.queryset.get(pk=collection_pk, user=request.user)
        except RecipeCollection.DoesNotExist:
            user_data = {
                'ussername': request.user.username,
                'id': request.user.id
            }
            return Response({'message': 'Recipe Collection does not exist.', 'user': user_data}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            recipe = Recipe.objects.get(pk=recipe_pk)
        except Recipe.DoesNotExist:
            return Response({'message': 'Recipe does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        RecipeCollectionRecipe.objects.filter(collection=collection, recipe=recipe).delete()
        return Response({'message': 'Recipe removed from collection sucessfully'}, status=status.HTTP_204_NO_CONTENT)