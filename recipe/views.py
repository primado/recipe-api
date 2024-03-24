from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import *


# Create your views here.

# Recipe CRUD View
@extend_schema(
    tags=['Recipe']
)
class RecipeView(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, recipe_id, user):
        recipe_id = self.kwargs.get('pk')
        user = self.request.user
        try:
            return self.queryset.get(id=recipe_id, user=user)
        except Recipe.DoesNotExist:
            return None

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Recipe List',
    )
    def list(self, request):
        user = request.user
        queryset = self.queryset.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Request Ok successful', 'data': serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        request=RecipeSerializer,
        responses={201: RecipeSerializer},
        description='Create Recipe'
    )
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
                return Response({'message': 'Recipe created successfully', 'data': serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'User Unauthorized'}, content_type='multipart/form-data',
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Update Recipe'
    )
    def update(self, request, pk=None, *args, **kwargs):
        recipe_instance = self.get_object(pk, request.user.id)

        if not recipe_instance:
            return Response({'message': 'Recipe does doest not exist'}, status=status.HTTP_404_NOT_FOUND)

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

        serializer = self.get_serializer(instance=recipe_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Recipe updated successfully', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        description='Delete Recipe'
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        recipe_instance = self.get_object(pk, request.user.id)

        if not recipe_instance:
            return Response({"message": 'Recipe does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        recipe_instance.delete()
        return Response({"message": 'Recipe deleted'}, status=status.HTTP_204_NO_CONTENT)


# Show Public Recipes to all users
@extend_schema(
    tags=['Recipe View']
)
class RecipeFeedView(APIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Recipe Feed/ Public Recipes'
    )
    def get(self, request):
        visibility = 'public'
        queryset = self.queryset.filter(visibility=visibility)
        if not queryset.exists():
            return Response({'message': 'There are no public recipes'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset, many=True)
        return Response({'message': 'Public recipes', 'data': serializer.data}, status=status.HTTP_200_OK)


# show private recipes to Recipes author/user
@extend_schema(
    tags=['User Private Recipes']
)
class UserPrivateRecipes(GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Private Recipes'
    )
    @action(detail=False, methods=['get'])
    def user_private_recipes(self, request):
        visibility = 'private'
        queryset = self.queryset.filter(visibility=visibility, user=request.user)
        if not queryset.exists():
            return Response({'message': 'There are no private recipes for you.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        return Response({'message': 'Your private recipes', 'data': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Recipe Collection']
)
class RecipeCollectionView(ModelViewSet):
    queryset = RecipeCollection.objects.all()
    serializer_class = RecipeCollectionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except RecipeCollection.DoesNotExist:
            return None

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Collection List'
    )
    def list(self, request):
        user = request.user
        queryset = self.queryset.filter(user=user)
        if not self.queryset.exists():
            return Response({'message': 'Recipe collection empty.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Request successful', 'data': serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        request=RecipeSerializer,
        responses={201: RecipeSerializer},
        description='Create Collection'
    )
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
                return Response({'message': 'Recipe collection created successfully', 'data': serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'User Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Update Collection'
    )
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
                return Response({'message': 'Recipe collection updated successfully', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response({'message': 'User unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeCollectionSerializer,
        description='Delete Collection',
    )
    def destroy(self, request, pk, *args, **kwargs):
        collection_instance = self.get_object(pk)
        if not collection_instance:
            return Response({'message': 'Recipe Collection does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        user_id_from_request = collection_instance.user.id
        if request.user.id != user_id_from_request:
            return Response({'message': 'User unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        collection_instance.delete()
        return Response({'message': 'Recipe collection deleted'}, status=status.HTTP_204_NO_CONTENT)

    # Views for adding and deleting a recipe to and from collection upon a request

    @extend_schema(
        tags=['Add Recipe to Collection Inline'],
        description='Add Recipe to Collection directly',
        responses={201: RecipeSerializer},
    )
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

        collection.recipe.add(recipe_serializer.instance, through_defaults=True)
        return Response({'message': 'Recipe added to collection successfully.', 'data': recipe_serializer.data},
                        content_type='multipart/form-data', status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Add Recipe to Collection Inline'],
        description='Delete Recipe from Collection Directly',
        request=RecipeSerializer,
    )
    def remove_recipe(self, request, *args, **kwargs):
        collection_pk = kwargs.get('pk')
        recipe_pk = self.kwargs.get('recipe_pk')
        try:
            collection = self.queryset.get(pk=collection_pk, user=request.user)
        except RecipeCollection.DoesNotExist:
            user_data = {
                'username': request.user.username,
                'id': request.user.id
            }
            return Response({'message': 'Recipe Collection does not exist.', 'user': user_data},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            recipe = Recipe.objects.get(pk=recipe_pk)
        except Recipe.DoesNotExist:
            return Response({'message': 'Recipe does not exist'}, status=status.HTTP_404_NOT_FOUND)
        RecipeCollectionRecipe.objects.filter(collection=collection, recipe=recipe).delete()
        return Response({'message': 'Recipe removed from collection successfully'}, status=status.HTTP_204_NO_CONTENT)


# Comment View
@extend_schema(
    tags=['Comment'],
    description='Add comments to public recipes.'
)
class CommentView(GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def get_serializer_class(self):
        return CommentSerializer

    @extend_schema(
        description='List Comments for a Particular recipe',
        responses={200: CommentSerializer},
        request=CommentSerializer,
    )
    def list(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')
        recipe = get_object_or_404(Recipe, pk=recipe_pk, visibility='public')
        # queryset = Comment.objects.get(recipe=recipe)
        queryset = self.get_queryset().filter(recipe=recipe)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response({'message': 'Request Successful', 'data': serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        request=CommentSerializer,
        responses={201: CommentSerializer},
        description='Create a comment'
    )
    def create(self, request, recipe_pk):
        recipe_pk = recipe_pk
        try:
            recipe = Recipe.objects.get(pk=recipe_pk, visibility='public')
        except Recipe.DoesNotExist:
            return Response({'message': 'Recipe does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        data = {
            'text': request.data.get('text'),
            'recipe': recipe_pk,
            'user': request.user.id
        }
        comment_data = data
        if not comment_data:
            return Response({'message': 'Text field cannot be blank'}, status=status.HTTP_400_BAD_REQUEST)

        comment_serializer_class = self.get_serializer_class()
        comment_serializer = comment_serializer_class(data=comment_data)

        if comment_serializer.is_valid():
            if request.user.id == data['user']:
                comment_serializer.save()
                return Response({'message': 'Comment created successfully', 'data': comment_serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, recipe_pk, comment_pk, *args, **kwargs):
        recipe_pk = recipe_pk
        comment_pk = comment_pk
        comment_instance = self.queryset.get(pk=comment_pk, recipe=recipe_pk)
        try:
            recipe = Recipe.objects.get(pk=recipe_pk, visibility='public')
        except Recipe.DoesNotExist:
            return Response({'message': 'Recipe does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        data = {
            'text': request.data.get('text'),
            'recipe': recipe_pk,
            'user': request.user.id
        }
        comment_serializer = self.serializer_class(comment_instance, data=data)
        if comment_serializer.is_valid():
            if request.user.id == comment_instance.user_id:
                comment_serializer.save()
                return Response({'message': 'Comment updated successfully.', 'data': comment_serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'User does not exist.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CommentSerializer,
        responses={201: CommentSerializer},
        description='Delete a comment'
    )
    def destroy(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')
        comment_pk = self.kwargs.get('comment_pk')
        comment_instance = self.get_queryset().get(pk=comment_pk, recipe=recipe_pk)
        if not comment_instance:
            return Response({'message': 'Comment doest not exist.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.id != comment_instance.user_id:
            return Response({'message': 'User is forbidden'}, status=status.HTTP_403_FORBIDDEN)
        else:
            comment_instance.delete()
        return Response({'message': 'Comment deleted'}, content_type='application/json',
                        status=status.HTTP_204_NO_CONTENT)
