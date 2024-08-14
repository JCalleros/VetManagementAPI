from django.urls import path
from .views import OwnerListAPIView, OwnerCreateAPIView, OwnerDetailAPIView

urlpatterns = [
    path("", OwnerListAPIView.as_view(), name="owner-list"),
    path("create/", OwnerCreateAPIView.as_view(), name="owner-create"),
    path("<uuid:id>/", OwnerDetailAPIView.as_view(), name="owner-detail"),
]