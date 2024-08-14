from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class OwnersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.owners"
    verbose_name = _("Owners")
