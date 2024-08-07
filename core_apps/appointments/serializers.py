from rest_framework import serializers
from .models import Appointment
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from core_apps.patients.serializers import PatientSerializer
from core_apps.patients.models import Patient

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'status', 'notes', 'date', 'service_type', 'patient']
    
    def validate_date(self, value):
        patient_uuid = self.initial_data.get('patient')
        if not patient_uuid:
            raise ValidationError("Patient ID is required.")
        
        patient = Patient.objects.get(id=patient_uuid)
        if Appointment.objects.filter(patient=patient, date=value).exists():
            raise ValidationError("An appointment already exists for this patient at the specified date and time.")
        return value
        
    def create(self, validated_data):
        patient_uuid = self.initial_data.get('patient')
        patient = Patient.objects.get(id=patient_uuid)
        try:
            appointment = Appointment.objects.create(**validated_data, patient=patient)
        except IntegrityError: 
            raise ValidationError({"detail": "Duplicate appointment"})
        return appointment