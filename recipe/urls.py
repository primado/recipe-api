from django.urls import path
from rest_framework.routers import DefaultRouter
from . views import *


router = DefaultRouter()
router.register(r'recipe', RecipeView)


urlpatterns = [
    path('feed/', RecipeFeedView.as_view(), name="feed")
]

urlpatterns += router.urls
