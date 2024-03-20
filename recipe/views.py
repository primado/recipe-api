from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class RecipeView(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self, recipe_id, user):
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
            serializer.save()
            return Response({'message': 'Recipe created successfully', 'data': serializer.data},  status=status.HTTP_201_CREATED)
        else:
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
        
