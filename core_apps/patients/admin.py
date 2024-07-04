from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["id", "species", "sex", "age_years", "age_months", "age_weeks"]
    list_display_links = ["id"]
    list_filter = ["species"]
