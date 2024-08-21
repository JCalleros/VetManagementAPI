from django.contrib import admin
from .models import Appointment

    
@admin.register(Appointment)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('status', 'date', 'service_type', 'get_patients')
    list_filter = ('status', 'service_type', 'date', 'patients')

    def get_patients(self, obj):
        return ", ".join([patient.name for patient in obj.patients.all()])
    
    get_patients.short_description = "Patients"