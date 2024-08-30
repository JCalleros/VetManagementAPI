import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("vet_management")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update_appointment_status': {
        'task': 'core_apps.appointments.tasks.update_appointment_status',
        'schedule': crontab(minute='*/15'),
    },
}