from rest_framework import serializers
from .models import Appointment
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from core_apps.patients.serializers import PatientSerializer
from core_apps.patients.models import Patient

class AppointmentSerializer(serializers.ModelSerializer):
    patients = PatientSerializer(read_only=True, many=True)

    class Meta:
        model = Appointment
        fields = ['id', 'status', 'notes', 'date', 'service_type', 'patients']
    
    def validate_date(self, value):
        patient_uuids = self.initial_data.get('patients')
        if not patient_uuids:
            raise ValidationError("At least one Patient ID is required.")
        
        for patient_uuid in patient_uuids:
            patient = Patient.objects.get(id=patient_uuid)
            if Appointment.objects.filter(patients=patient, date=value).exists():
                raise ValidationError("An appointment already exists for this patient at the specified date and time.")
        return value
        
    def create(self, validated_data):
        patient_uuids = self.initial_data.get('patients')
        patients = Patient.objects.filter(id__in=patient_uuids)
        try:
            appointment = Appointment.objects.create(**validated_data)
            appointment.patients.set(patients)
            appointment.save()
        except IntegrityError: 
            raise ValidationError({"detail": "Duplicate appointment"})
        return appointment
    

class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be greater than start date.")
        return data