from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import  ModelViewSet
from rest_framework.views import APIView
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema
# from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView , PasswordChangeView, PasswordResetConfirmView,
# PasswordResetView
from .serializers import *

# Create your views here.


@extend_schema(
    tags=['User Profile View '],
    description='Profile View',
)
class UserProfileUpdateView(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateCustomUserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        tags=['Profile List'],
        description='List Profile details',
        responses={200: UpdateCustomUserSerializer}
    )
    def list(self, request, *args, **kwargs):
        user = request.user.id
        queryset = CustomUser.objects.filter(id=user)
        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)

    @extend_schema(
            tags=['Update User Account'],
            responses = {200: UpdateCustomUserSerializer},
            description = 'Update User Account Endpoint'
    )
    def partial_update(self, request, *args, **kwargs):

        try:
            user_instance = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        update_data = {
            'id': user_instance.id,
            'username': request.data.get('username'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'bio': request.data.get('bio'),
            'headline': request.data.get('headline'),
            'instagram': request.data.get('instagram'),
            'facebook': request.data.get('facebook'),
            'website': request.data.get('website'),
        }

        serializer = self.get_serializer(data=update_data, instance=user_instance, partial=True)
        if serializer.is_valid():
            if request.user.id == user_instance.id:
                serializer.save()
                return Response({'detail': 'User updated successfully', 'data': serializer.data},
                                content_type='multipart/form-data', status=status.HTTP_200_OK)
            return Response({'detail': 'user forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccount(ModelViewSet):
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    serializer_class = DeleteAccountSerializer

    def get_object(self, username):
        username = self.kwargs.get(self.lookup_field)
        return self.queryset.get(username=username)

    @extend_schema(
            tags=['Delete User Account'],
            description='Delete Account of User',
    )
    def destroy(self, request, username=None):
        try:
            user = self.get_object(username=username)
            user.delete()
            return Response({'message': 'Your account has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Account does not exist'}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['Profile Picture View'],
    description='Profile Picture View'
)
class ProfilePictureView(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfilePictureSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(id=request.user.id)
        serializer = ProfilePictureSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     picture_data = {
    #         "id": request.user.id,
    #         "profile_picture": request.data['profile_picture'],
    #     }
    #     serializer = ProfilePictureSerializer(data=picture_data)
    #     if serializer.is_valid():
    #         if request.user.id == picture_data['id']:
    #             serializer.save()
    #             return Response(serializer.data, content_type='multipart/form-data', status=status.HTTP_201_CREATED)
    #         return Response({'detail': 'User authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update(self, request, *args, **kwargs):
    try:
        user_instance = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    picture_data = {
        "id": request.user.id,
        "profile_picture": request.data.get('profile_picture'),
    }
    serializer = ProfilePictureSerializer(data=picture_data, partial=True, instance=user_instance)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, content_type='multipart/form-data', status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def destroy(self, request, *args, **kwargs):
    user = request.user
    if not user.profile_picture:
        return Response({'detail': 'User does not have a profile picture'}, status=status.HTTP_404_NOT_FOUND)
    user.profile_picture.delete()
    user.profile.delete = None
    user.save()
    return Response({'detail': 'Profile picture deleted'}, status=status.HTTP_200_OK)




