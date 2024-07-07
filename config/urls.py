from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Vet Management",
        default_version="v1",
        description="A vet management system",
        contact=openapi.Contact(email="calleros.dev@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.users.urls")),
    path("api/v1/patients/", include("core_apps.patients.urls")),
    path("api/v1/owners/", include("core_apps.owners.urls")),
]

admin.site.site_header = "Vet Management Admin"
admin.site.site_title = "Vet Management Admin Portal"
admin.site.index_title = "Welcome to Vet Management Admin Portal"
