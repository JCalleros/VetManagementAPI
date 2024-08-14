import cloudinary
from uuid import UUID
from celery import shared_task
from .models import Patient

@shared_task(name="upload_photo_to_cloudinary")
def upload_photo_to_cloudinary(patient_id: UUID, image_content: bytes) -> None:
    patient = Patient.objects.get(id=patient_id)
    response = cloudinary.uploader.upload(image_content)
    patient.photo = response["url"]
    patient.save()