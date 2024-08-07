from django.contrib import admin
from .models import Appointment

    
@admin.register(Appointment)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('status', 'date', 'service_type', 'patient')
    list_filter = ('status', 'service_type', 'date', 'patient')
