from django.db import models
from django.utils.translation import gettext_lazy as _
from core_apps.common.models import TimeStampedModel
from core_apps.patients.models import Patient


class Appointment(TimeStampedModel):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', _('Scheduled')
        COMPLETED = 'completed', _('Completed')
        CANCELED = 'canceled', _('Canceled')

    patients = models.ManyToManyField(Patient, verbose_name=_("Patients"), related_name='appointments')
    date = models.DateTimeField()
    service_type = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment for {self.patient.name} on {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")