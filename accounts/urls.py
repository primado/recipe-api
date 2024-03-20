from django.urls import path, include
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from dj_rest_auth.jwt_auth import get_refresh_view
from rest_framework_simplejwt.views import TokenVerifyView, TokenBlacklistView
from . views import UserProfileUpdateView, DeleteAccount
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'update-profile', UserProfileUpdateView)
router.register(r'delete-account', DeleteAccount)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('user/', UserDetailsView.as_view(), name="user-details"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path('token/blacklist', TokenBlacklistView.as_view(), name="token-blacklist"),



]


