from rest_framework import serializers
from .models import CustomUser


# Create your serializers here

class CustomUserSerializers(serializers.ModelSerializer):

    class Meta: 
        model = CustomUser
        fields = '__all__'


class UpdateCustomUserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = CustomUser
        fields = ('id', 'username', 'bio', 'headline', 'instagram', 'facebook', 'website')

class DeleteAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


