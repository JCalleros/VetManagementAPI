from django.db import models
from django.utils.translation import gettext_lazy as _
from core_apps.common.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
from core_apps.owners.models import Owner
from autoslug import AutoSlugField


class Patient(TimeStampedModel):
    class Gender(models.TextChoices):
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
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=20,
        choices=Gender.choices,
        default=Gender.Male
    )
    breed = models.CharField(max_length=150, null=True, blank=True)
    age_years = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(200)])
    age_months = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(11)])
    age_weeks = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(52)])
    color = models.CharField(max_length=100, null=True, blank=True)
    photo = CloudinaryField(verbose_name=_("Photo"), blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, verbose_name=_("Owner"), related_name='patients')
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self) -> str:
        return f"{self.name}"        
    
    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        unique_together = ('name', 'species', 'gender', 'owner')
