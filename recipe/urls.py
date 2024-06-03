from django.urls import path
from rest_framework.routers import DefaultRouter
from . views import *


router = DefaultRouter()
# router.register(r'recipe', RecipeView)
# router.register(r'collection', RecipeCollectionView)


urlpatterns = [
    path('recipe',RecipeView.as_view({'get': 'list', 'post': 'create'})),
    path('public-recipe', RecipeView.as_view({'get': 'publicRecipe'})),
    path('recipe/<int:recipe_pk>', RecipeView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('feed/', RecipeFeedView.as_view({'get': 'list'}), name="feed"),
    path('feed/<int:recipe_pk>', RecipeFeedView.as_view({'get': 'retrieve'}), name="feed"),
    path('private-recipes/', UserPrivateRecipes.as_view({'get': 'user_private_recipes'}), name="private-recipes"),
    path('collection/<int:pk>/add-recipe', RecipeCollectionView.as_view({'post': 'add_recipe'}),
         name='add_recipe_collection'),

    path('collection/<int:collection_pk>', RecipeCollectionView.as_view({'delete': 'destroy',  'put': 'update'}),
         name="collection"),

    # path('collection/<int:collection_pk>/<int:recipe_pk>',
    #      RecipeCollectionView.as_view({'delete': 'remove_recipe'}), name='remove-recipe-collection'),

    path('collection', RecipeCollectionView.as_view({'post': 'create_collection', 'get': 'list'}),
         name='create_collection'),

    path('recipe/<int:recipe_pk>/comment', CommentView.as_view({'get': 'list', 'post': 'create'})),
    path('recipe/<int:recipe_pk>/comment/<int:comment_pk>',
         CommentView.as_view({'put': 'update', 'delete': 'destroy'})),

    # RECIPE RATING
    path('recipe/<int:recipe_pk>/rating', RecipeRatingView.as_view({'get': 'list', 'post': 'create'})),
    path('recipe/<int:recipe_pk>/rating/<int:rating_pk>', RecipeRatingView.as_view({'put': 'update',
                                                                                    'delete': 'destroy'})),

    # Comment Rating URLS
    path('comment/<int:comment_pk>/rating', CommentRatingView.as_view({'get': 'list', 'post': 'create'})),
    path('comment/<int:comment_pk>/rating/<int:comment_vote_pk>', CommentRatingView.as_view({'put': 'update',
                                                                                             'delete': 'destroy'})),

    path('check-usernmae/<str:username>', CheckUserName.as_view({'get': 'retrieve'}), name='check-username')




]

urlpatterns += router.urls
