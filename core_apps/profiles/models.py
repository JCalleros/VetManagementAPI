from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    class Occupation(models.TextChoices):
        Vet = (
            "vet",
            _("Vet"),
        )
        Assistant = (
            "assistant",
            _("Assistant"),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = CloudinaryField(verbose_name=_("Avatar"), blank=True, null=True)
    occupation = models.CharField(
        verbose_name=_("Occupation"),
        max_length=20,
        choices=Occupation.choices,
        default=Occupation.Vet
    )
    
    phone_numbe = PhoneNumberField(verbose_name=_("Phone Number"), max_length=30, default="+545532098725")
