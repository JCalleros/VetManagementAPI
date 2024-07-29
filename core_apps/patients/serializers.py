from rest_framework import serializers
from core_apps.owners.models import Owner
from .models import Patient
from core_apps.owners.serializers import OwnerSerializer


class PatientSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'name', 'species', 'gender', 'breed', 'age_years', 'age_months', 'age_weeks', 'color', 'photo', 'slug', 'owner']


    def create(self, validated_data):
        owner_uuid = self.initial_data.get('owner')
        owner = Owner.objects.get(id=owner_uuid)
        patient = Patient.objects.create(**validated_data, owner=owner)
        return patient
    
    def update(self, instance, validated_data):
        owner_uuid = validated_data.pop('owner', None)
        if owner_uuid:
            owner = Owner.objects.get(id=owner_uuid)
            instance.owner = owner
        return super().update(instance, validated_data)