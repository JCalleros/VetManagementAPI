from django.shortcuts import render
from rest_framework import generics, permissions, filters
from ..common.renderers import GenericJSONRenderer
from .models import Owner
from .serializers import OwnerSerializer
from .permissions import CanCreateEditOwner
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import CanCreateEditOwner

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
    queryset = Owner.objects.order_by('-created_at')

class OwnerCreateAPIView(generics.CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [CanCreateEditOwner]
    object_label = "owner"
    
class OwnerDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OwnerSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]
    object_label = "owner"
    lookup_field = 'id'

    def get_queryset(self):
        return Owner.objects.filter(id=self.kwargs[self.lookup_field])
    
    def get_object(self) -> Owner:
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        owner = generics.get_object_or_404(queryset, **filter_kwargs)
        return owner