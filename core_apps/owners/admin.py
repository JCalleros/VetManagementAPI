from django.contrib import admin
from .models import Owner

# Register your models here.
@admin.register(Owner)
class OwnerProfile(admin.ModelAdmin):
    list_display = ["id", "name", "phone_number", "email"]