from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from core_apps.apartments.serializers import ApartmentSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.first_name")
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            "id",
            "slug",
            "name",
            "occupation",
            "date_joined",
            "avatar",
        ]

    def get_avatar(self, obj: Profile) -> str | None:
        try:
            return obj.avatar.url
        except AttributeError:
            return None


class UpdateProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")
    
    class Meta:
        model = Profile
        fields = [
            "name",
            "occupation",
            "phone_number",
        ]


class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]