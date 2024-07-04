from django.urls import path
from .views import PatientListAPIView, PatientCreateAPIView

urlpatterns = [
    path("", PatientListAPIView.as_view(), name="patient-list"),
    path("create/", PatientCreateAPIView.as_view(), name="patient-create")
]