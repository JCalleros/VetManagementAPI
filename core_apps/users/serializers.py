from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "name", "password"]
        
class CustomUserSerializer(UserSerializer):
    occupation = serializers.ReadOnlyField(source='profile.occupation')
    phone_number = PhoneNumberField(source='profile.phone_number')
    avatar = serializers.ReadOnlyField(source='profile.avatar.url')
    
    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            "id", "email", "name", "occupation", "phone_number", 
            "avatar", "data_joined",
        ]
        read_only_fields = ["id", "email", "date_joined"]

    