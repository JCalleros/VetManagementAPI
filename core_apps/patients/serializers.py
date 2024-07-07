from rest_framework import serializers
from core_apps.owners.models import Owner
from .models import Patient



class PatientSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    owner_phone_number = serializers.CharField(source='owner.phone_number', read_only=True)
    
    
    class Meta:
        model = Patient
        fields = ["id", "name", "species", "gender", "owner", "owner_name", "owner_phone_number", "created_at"]

