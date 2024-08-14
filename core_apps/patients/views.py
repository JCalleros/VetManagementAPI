from django.http import Http404
from rest_framework import generics, permissions, filters
from ..common.renderers import GenericJSONRenderer
from .models import Patient
from .serializers import PatientSerializer
from .permissions import CanCreateEditPatient, CanDeletePatient
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 20


class PatientListAPIView(generics.ListAPIView):
    serializer_class = PatientSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    object_label = "patients"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "owner__name", "owner__phone_number"]
    filterset_fields = ["gender", "species"]
    queryset = Patient.objects.order_by('-created_at')


class PatientDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "patient"
    lookup_field = "id"
    
    def get_queryset(self):
        return Patient.objects.filter(id=self.kwargs[self.lookup_field])

    def get_object(self) -> Patient:
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        patient = generics.get_object_or_404(queryset, **filter_kwargs)
        return patient

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
    lookup_field = "id"


class PatientDeleteAPIView(generics.DestroyAPIView):
    queryset = Patient.objects.all()
    lookup_field = "id"
    serializer_class = PatientSerializer
    permission_classes = [CanDeletePatient]

    def get_object(self) -> Patient:
        try:
            patient = super().get_object()
        except Http404:
            raise Http404("Patient not found") from None
        return patient

    def delete(self, request, *args, **kwargs) -> Response:
        super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)