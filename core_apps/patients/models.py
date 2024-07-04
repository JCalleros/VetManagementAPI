from django.db import models
from django.utils.translation import gettext_lazy as _
from core_apps.common.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
from core_apps.owners.models import Owner

class Patient(TimeStampedModel):
    class Sex(models.TextChoices):
        Male = (
            "male",
            _("Male"),
        )
        Female = (
            "female",
            _("Female"),
        )

    name = models.CharField(max_length=100, db_index=True)
    species = models.CharField(max_length=100)
    sex = models.CharField(
        verbose_name=_("Sex"),
        max_length=20,
        choices=Sex.choices,
        default=Sex.Male
    )
    breed = models.CharField(max_length=150, null=True, blank=True)
    age_years = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(200)])
    age_months = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(12)])
    age_weeks = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(52)])
    
    color = models.CharField(max_length=100, null=True, blank=True)
    photo = CloudinaryField(verbose_name=_("Photo"), blank=True, null=True)
    owners = models.ManyToManyField(Owner, verbose_name=_("Owner"), blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_age(self) -> str:
        return f"{self.age_years} years {self.age_months} months {self.age_weeks} weeks"
    
    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")