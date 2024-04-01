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
class RecipeView(GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Recipe List View',
    )
    def list(self, request):
        user = request.user
        queryset = self.queryset.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Request Ok successful', 'data': serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description="Recipe Detail View"
    )
    def retrieve(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')
        try:
            recipe = Recipe.objects.get(pk=recipe_pk)
        except Recipe.DoesNotExist:
            return Response({'detail': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(recipe)
        if request.user == recipe.user:
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        elif request.user != recipe.user_id and recipe.visibility == 'private':
            return Response({'message': 'You do not have permission to access this private recipe.'},
                            status=status.HTTP_403_FORBIDDEN)

        elif recipe.visibility == 'public':
            return Response({'data': serializer.data},
                            status=status.HTTP_200_OK)
        # Handle unexpected cases
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        responses={201: RecipeSerializer},
        description='Create Recipe View'
    )
    def create(self, request):

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

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            if request.user.id == data['user']:
                serializer.save()
                return Response({'message': 'Recipe created successfully', 'data': serializer.data},
                                content_type='multipart/form-data',
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'User Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Update Recipe View'
    )
    def update(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')
        recipe_instance = Recipe.objects.get(pk=recipe_pk, user=request.user)

        if not recipe_instance:
            return Response({'message': 'Recipe does doest not exist'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'id': recipe_pk,
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
            if request.user.id == recipe_instance.user.id:
                serializer.save()
                return Response({'data': serializer.data}, content_type='multipart/form-data',
                                status=status.HTTP_200_OK)
            return Response({'message': 'User forbidden'}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        description='Delete Recipe View'
    )
    def destroy(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')
        recipe_instance = self.queryset.filter(pk=recipe_pk, user=request.user)

        if not recipe_instance:
            return Response({"message": 'Recipe does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        recipe_instance.delete()
        return Response({"message": 'Recipe deleted'}, status=status.HTTP_204_NO_CONTENT)


# Show Public Recipes to all users
@extend_schema(
    tags=['Recipe Feed View'],
    description='Public Recipe Feeds'
)
class RecipeFeedView(APIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Recipe Feed/ Public Recipes'
    )
    def get(self, request):
        visibility = 'public'
        queryset = self.queryset.filter(visibility=visibility)
        if not queryset.exists():
            return Response({'message': 'Public recipes not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


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
        description='Private Recipes View'
    )
    @action(detail=False, methods=['get'])
    def user_private_recipes(self, request):
        visibility = 'private'
        queryset = self.queryset.filter(visibility=visibility, user=request.user)
        if not queryset.exists():
            return Response({'message': 'Private recipes not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(
    tags=['Recipe Collection']
)
class RecipeCollectionView(ModelViewSet):
    queryset = RecipeCollection.objects.all()
    serializer_class = RecipeCollectionSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Collection List View'
    )
    def list(self, request):
        user = request.user
        queryset = self.queryset.filter(user=user)
        if not self.queryset.exists():
            return Response({'message': 'Recipe collection empty.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, content_type='application/json',
                        status=status.HTTP_200_OK)

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
            return Response({'message': 'User Unauthorized'}, content_type='application/json',
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeSerializer},
        description='Update Collection'
    )
    def update(self, request, pk, *args, **kwargs):
        collection_instance = RecipeCollection.objects.filter(pk=pk, user=request.user)
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'user': request.user.id
        }

        if not collection_instance:
            return Response({'message': 'Recipe Collection does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=collection_instance, data=data)
        if serializer.is_valid():
            if request.user.id == data['user']:
                serializer.save()
                return Response({'message': 'Recipe collection updated successfully', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response({'message': 'User unauthorized'}, content_type='application/json',
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeCollectionSerializer,
        description='Delete Collection',
    )
    def destroy(self, request, pk, *args, **kwargs):
        collection_instance = RecipeCollection.objects.filter(pk=pk, user=request.user)
        if not collection_instance:
            return Response({'message': 'Recipe Collection does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        user_id_from_request = collection_instance.get(user=request.user)
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
        return Response({'data': recipe_serializer.data},
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

        return Response({'message': 'Recipe removed from collection successfully'},
                        status=status.HTTP_204_NO_CONTENT)


# Comment View
@extend_schema(
    tags=['Comment'],
    description='Add comments to public recipes.'
)
class CommentView(GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

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
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

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

    @extend_schema(
        request=CommentSerializer,
        responses={200: CommentSerializer},
        description='Update a comment View'
    )
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
        comment_serializer = self.serializer_class(instance=comment_instance, data=data)
        if comment_serializer.is_valid():
            if request.user.id == comment_instance.user_id:
                comment_serializer.save()
                return Response({'message': 'Comment updated successfully.', 'data': comment_serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'User does not exist.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CommentSerializer,
        responses={204: CommentSerializer},
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


# RECIPE RATING VIEW
@extend_schema(
    tags=['Rate Recipe'],
    description='Upvote or Downvote a Recipe.'
)
class RecipeRatingView(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.all()

    def get_serializer_class(self):
        return RecipeRatingSerializer

    @extend_schema(
        description='Get the number of Rating Counts for a Recipe',
        responses={200: RecipeRatingSerializer},
        request=RecipeSerializer,
    )
    def list(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')  # recipe_pk is a parameter
        upvote_count = self.get_queryset().filter(recipe=recipe_pk, vote_type=Rating.UPVOTE).count()
        downvote_count = self.get_queryset().filter(recipe=recipe_pk, vote_type=Rating.DOWNVOTE).count()
        return Response({'upvote_count': upvote_count,
                         'downvote_count': downvote_count}, status=status.HTTP_200_OK)

    @extend_schema(
        request=RecipeRatingSerializer,
        responses={201: RecipeRatingSerializer},
        description='Rate a Recipe i.e. either upvote or downvote'
    )
    def create(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')  # recipe_pk is a parameter

        data = {
            'user': request.user.id,
            'recipe': recipe_pk,
            'vote_type': request.data.get('vote_type')
        }
        recipe = Recipe.objects.filter(pk=recipe_pk)
        if not recipe.exists():
            return Response({'message': 'Recipe does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        create_serializer = self.get_serializer_class()
        serializer = create_serializer(data=data)
        if serializer.is_valid():
            if request.user.id == data['user']:
                serializer.save()
                return Response({'data': serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'User forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeSerializer,
        responses={200: RecipeRatingSerializer},
        description='Update a Rating on a Recipe'
    )
    def update(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')  # recipe_pk is a parameter
        rating_pk = self.kwargs.get('rating_pk')  # rating_pk is a parameter

        try:
            rating = self.get_queryset().get(pk=rating_pk, recipe=recipe_pk, user=request.user)
        except Rating.DoesNotExist:
            return Response({'message': 'Rating does not exist'}, status=status.HTTP_404_NOT_FOUND)

        vote_type = request.data.get("vote_type")
        if vote_type not in [Rating.UPVOTE, Rating.DOWNVOTE]:
            return Response({'message': 'Invalid vote type'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'recipe': recipe_pk,
            'user': request.user.id,
            'vote_type': vote_type,
        }
        rating_serializer = self.get_serializer_class()
        serializer = rating_serializer(instance=rating, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RecipeRatingSerializer,
        responses={204: RecipeRatingSerializer},
        description='Delete a Rating'
    )
    def destroy(self, request, *args, **kwargs):
        recipe_pk = self.kwargs.get('recipe_pk')  # recipe_pk is a parameter
        rating_pk = self.kwargs.get('rating_pk')  # rating_pk is a parameter

        try:
            rating = self.get_queryset().filter(pk=rating_pk, recipe=recipe_pk, user=request.user)
        except Rating.DoesNotExist:
            return Response({'message': 'Vote type does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if rating.exists():
            rating.delete()
            return Response({'message': 'Vote type deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Vote type does not exist'}, status=status.HTTP_400_BAD_REQUEST)


# Comment Rating

class CommentRatingView(GenericViewSet):
    queryset = CommentVote.objects.all()
    serializer_class = CommentVoteSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        comment_pk = self.kwargs.get('comment_pk')  # comment is a parameter
        upvote_count = self.get_queryset().filter(pk=comment_pk, vote_type=CommentVote.UPVOTE).count()
        downvote_count = self.get_queryset().filter(pk=comment_pk, vote_type=CommentVote.DOWNVOTE).count()

        data = {
            "upvote_count": upvote_count,
            "downvote_count": downvote_count
        }
        return Response({'data': {'upvote_count': upvote_count,
                                  'downvote_count': downvote_count}}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        comment_pk = self.kwargs.get('comment_pk')

        data = {
            "user": request.user.id,
            "comment": comment_pk,
            "vote_type": request.data.get('vote_type')
        }

        comment = Comment.objects.filter(pk=comment_pk)
        if not comment.exists():
            return Response({'message': "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        comment_vote_serializer = self.get_serializer_class()
        serializer = comment_vote_serializer(data=data)
        if serializer.is_valid():
            if request.user.id == data['user']:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'User unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        comment_pk = self.kwargs.get('comment_pk')
        comment_vote_pk = self.kwargs.get('comment_vote_pk')

        try:
            comment_vote = CommentVote.objects.get(pk=comment_vote_pk, comment=comment_pk)
        except CommentVote.DoesNotExist:
            return Response({'message': 'Comment does found'}, status=status.HTTP_404_NOT_FOUND)

        vote_type = request.data.get('vote_type')
        if vote_type not in [CommentVote.UPVOTE, CommentVote.DOWNVOTE]:
            return Response({'message': 'Invalid vote type'}, status=status.HTTP_400_BAD_REQUEST)

        comment_vote_serializer = self.get_serializer_class()
        serializer = comment_vote_serializer(instance=comment_vote)
        if serializer.is_valid():
            if request.user.id == comment_vote.user.id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'User unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        comment_pk = self.kwargs.get('comment_pk')
        comment_vote_pk = self.kwargs.get('comment_vote_pk')

        comment_vote = CommentVote.objects.filter(pk=comment_vote_pk, comment=comment_pk)

        if comment_vote.exists():
            comment_vote.delete()
            return Response({'message': 'Vote type deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'vote type not found'}, status=status.HTTP_400_BAD_REQUEST)
