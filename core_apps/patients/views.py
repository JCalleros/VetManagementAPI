from django.shortcuts import render
from rest_framework import generics, permissions, filters
from ..common.renderers import GenericJSONRenderer
from .models import Patient
from .serializers import PatientSerializer
from .permissions import CanCreateEditPatient
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100


class PatientListAPIView(generics.ListAPIView):
    serializer_class = PatientSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    object_label = "patients"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "owner__name", "owner__phone_number"]
    filterset_fields = ["gender", "species"]
    queryset = Patient.objects.all()


class PatientDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "patient"


class PatientCreateAPIView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [CanCreateEditPatient]
    object_label = "patient"


class PatientUpdateAPIView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [CanCreateEditPatient]
    object_label = "patient"
