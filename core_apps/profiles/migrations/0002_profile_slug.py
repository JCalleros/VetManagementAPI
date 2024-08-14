# Generated by Django 5.0.6 on 2024-07-08 19:16

import autoslug.fields
import core_apps.profiles.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default=2,
                editable=False,
                populate_from=core_apps.profiles.models.get_user_email,
                unique=True,
            ),
            preserve_default=False,
        ),
    ]
