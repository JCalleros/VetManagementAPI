# Generated by Django 5.0.6 on 2024-07-06 03:46

import cloudinary.models
import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("owners", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(db_index=True, max_length=100)),
                ("species", models.CharField(max_length=100)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        default="male",
                        max_length=20,
                        verbose_name="Gender",
                    ),
                ),
                ("breed", models.CharField(blank=True, max_length=150, null=True)),
                (
                    "age_years",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(200),
                        ],
                    ),
                ),
                (
                    "age_months",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(11),
                        ],
                    ),
                ),
                (
                    "age_weeks",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(52),
                        ],
                    ),
                ),
                ("color", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "photo",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="Photo"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="patients",
                        to="owners.owner",
                        verbose_name="Owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Patient",
                "verbose_name_plural": "Patients",
                "unique_together": {("name", "species", "gender", "owner")},
            },
        ),
    ]
