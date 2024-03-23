from django.urls import path
from rest_framework.routers import DefaultRouter
from . views import *


router = DefaultRouter()
router.register(r'recipe', RecipeView)
router.register(r'collection', RecipeCollectionView)


urlpatterns = [
    path('feed/', RecipeFeedView.as_view(), name="feed"),
    path('private-recipes/', UserPrivateRecipes.as_view({'get': 'user_private_recipes'}), name="private-recipes"),
    path('collection/<int:pk>/add-recipe/', RecipeCollectionView.as_view({'post': 'add_recipe'}),
         name='add_recipe_collection'),

    path('collection/<int:pk>/<int:recipe_pk>/delete/', RecipeCollectionView.as_view({'delete': 'remove_recipe'}),
         name='remove-recipe-collection'),

    path('recipe/<int:recipe_pk>/comment/', CommentView.as_view({'get': 'list', 'post': 'create'})),
    path('recipe/<int:recipe_pk>/comment/<int:comment_pk>/', CommentView.as_view({'put': 'update'})),



]

urlpatterns += router.urls
