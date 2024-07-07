from django.db import models
from core_apps.common.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Owner(TimeStampedModel):
    name = models.CharField(max_length=100, db_index=True)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"), max_length=30, default="+545532098725", db_index=True)
    email = models.EmailField(verbose_name=_("Email Address"), blank=True, null=True, db_index=True)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = _("Owner")
        verbose_name_plural = _("Owners")