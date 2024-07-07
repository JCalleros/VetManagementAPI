from django.urls import path
from .views import OwnerListAPIView

urlpatterns = [
    path("", OwnerListAPIView.as_view(), name="owner-list"),
]