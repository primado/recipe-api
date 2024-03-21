from django.urls import path
from rest_framework.routers import DefaultRouter
from . views import *


router = DefaultRouter()
router.register(r'recipe', RecipeView)


urlpatterns = [
    path('feed/', RecipeFeedView.as_view(), name="feed"),
    path('private-recipes/', UserPrivateRecipes.as_view({'get': 'user_private_recipes'}), name="private-recipes")

]

urlpatterns += router.urls
