from django.urls import path, include
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import (LoginView, LogoutView, UserDetailsView, PasswordChangeView, PasswordResetConfirmView,
                                PasswordResetView)
from dj_rest_auth.jwt_auth import get_refresh_view
from rest_framework_simplejwt.views import TokenVerifyView, TokenBlacklistView
from . views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'update-profile', UserProfileUpdateView)
# router.register(r'delete-account', DeleteAccount)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('user/', UserDetailsView.as_view(), name="user-details"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path('token/blacklist', TokenBlacklistView.as_view(), name="token-blacklist"),


    path('delete-account/<str:username>/', DeleteAccount.as_view({'delete': 'destroy'})),

    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    path('user-profile', UserProfileUpdateView.as_view({'get': 'list'}), name='profile-list'),
    path('<str:username>/profile-update', UserProfileUpdateView.as_view({'patch': 'partial_update'}),
         name='user-details-patch'),

    # Profile Picture
    path('profile-picture', ProfilePictureView.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy'}),
         name='profile')

]


