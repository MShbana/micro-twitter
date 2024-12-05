"""Common App Models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Parent Class for all models."""

    class Meta:
        abstract = True
        default_permissions = ["add", "view", "change", "delete"]

    time_created = models.DateTimeField(
        verbose_name=_("time created"),
        auto_now_add=True,
    )
    time_updated = models.DateTimeField(
        verbose_name=_("time updated"),
        auto_now=True,
    )
