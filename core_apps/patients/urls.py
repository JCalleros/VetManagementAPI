from django.urls import path
from .views import PatientListAPIView, PatientCreateAPIView, PatientDetailAPIView, PatientUpdateAPIView, PatientDeleteAPIView

urlpatterns = [
    path("", PatientListAPIView.as_view(), name="patient-list"),
    path("create/", PatientCreateAPIView.as_view(), name="patient-create"),
    path("<uuid:id>/", PatientDetailAPIView.as_view(), name="patient-detail"),
    path("<uuid:id>/update/", PatientUpdateAPIView.as_view(), name="patient-update"),
    path("<uuid:id>/delete/", PatientDeleteAPIView.as_view(), name="patient-delete"),
]