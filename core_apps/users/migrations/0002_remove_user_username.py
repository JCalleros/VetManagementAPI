# Generated by Django 5.0.6 on 2024-06-30 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
