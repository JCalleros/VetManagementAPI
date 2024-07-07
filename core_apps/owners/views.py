from django.shortcuts import render
from rest_framework import generics, permissions, filters
from ..common.renderers import GenericJSONRenderer
from .models import Owner
from .serializers import OwnerSerializer
from .permissions import CanCreateEditOwner
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100


class OwnerListAPIView(generics.ListAPIView):
    serializer_class = OwnerSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    object_label = "owners"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "phone_number"]
    filterset_fields = ["name", "phone_number"]
    queryset = Owner.objects.all()
    