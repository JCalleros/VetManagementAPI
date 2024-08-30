from django.http import Http404
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import AppointmentSerializer
from core_apps.common.renderers import GenericJSONRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response 

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AppointmentListAPIView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    object_label = "appointments"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['patients', 'status', 'date']
    search_fields = ['service_type', 'status', 'notes']
    queryset = Appointment.objects.order_by('-created_at')


class AppointmentCreateAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "appointment"


class AppointmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    object_label = "appointment"


class AppointmentUpdateAPIView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]
    object_label = "appointment"
    lookup_field = "id"


class AppointmentDeleteAPIView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    lookup_field = "id"
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Appointment:
        try:
            appointment = super().get_object()
        except Http404:
            raise Http404("Appointment not found") from None
        return appointment

    def delete(self, request, *args, **kwargs) -> Response:
        super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)