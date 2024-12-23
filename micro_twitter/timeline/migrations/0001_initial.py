# Generated by Django 4.2.17 on 2024-12-05 02:12

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tweet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "time_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="time created"
                    ),
                ),
                (
                    "time_updated",
                    models.DateTimeField(auto_now=True, verbose_name="time updated"),
                ),
                (
                    "public_id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="123456789", length=22, max_length=22, prefix=""
                    ),
                ),
                ("content", models.CharField(max_length=140, verbose_name="content")),
            ],
            options={
                "abstract": False,
                "default_permissions": ["add", "view", "change", "delete"],
            },
        ),
    ]
