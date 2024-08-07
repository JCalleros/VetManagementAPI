from django.urls import path
from .views import AppointmentListAPIView, AppointmentCreateAPIView, AppointmentDetailAPIView, AppointmentUpdateAPIView ,AppointmentDeleteAPIView

urlpatterns = [
    path('', AppointmentListAPIView.as_view(), name='appointment-list'),
    path('create/', AppointmentCreateAPIView.as_view(), name='appointment-create'),
    path('<uuid:id>/', AppointmentDetailAPIView.as_view(), name='appointment-detail'),
    path("update/<uuid:id>/", AppointmentUpdateAPIView.as_view(), name="appointment-update"),
    path("delete/<uuid:id>/", AppointmentDeleteAPIView.as_view(), name="appointment-delete"),
]