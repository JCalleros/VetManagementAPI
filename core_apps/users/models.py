import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from core_apps.users.managers import UserManager

    
class User(AbstractUser):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=120)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True, db_index=True)
    username = None
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = [
        "name",
    ]
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]
        
    