from django.shortcuts import render
from rest_framework.viewsets import  ModelViewSet
from rest_framework.views import APIView
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

# Create your views here.

class UserProfileUpdateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateCustomUserSerializer
    lookup_field = 'username'

    def get_object(self):
        return self.request.user        

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class DeleteAccount(ModelViewSet):
    queryset = CustomUser.objects.all()
    lookup_field = 'username'

    def get_object(self, username):
        username = self.kwargs.get(self.lookup_field)
        return self.queryset.get(username=username)

    
    def destroy(self, request, username=None):
        try:
            user = self.get_object(username=username)
            user.delete()
            return Response({'message': 'Your account has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Account does not exist'}, status=status.HTTP_204_NO_CONTENT)
            
