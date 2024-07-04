from rest_framework import serializers
from core_apps.owners.models import Owner
from .models import Patient



class PatientSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(many=True, queryset=Owner.objects.all())
    
    class Meta:
        model = Patient
        fields = ["id", "name", "species", "sex", "owners", "created_at"]
