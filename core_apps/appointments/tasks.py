from celery import shared_task
from django.utils import timezone
from .models import Appointment

BATCH_SIZE = 10

@shared_task
def update_appointment_status():
    appointments = Appointment.objects.filter(date__lte=timezone.now() - timezone.timedelta(minutes=15), status=Appointment.Status.SCHEDULED)
    updated_count = 0
    for appointment in appointments:
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
        updated_count += 1
    
    return f"Updated {updated_count} appointments to COMPLETED"