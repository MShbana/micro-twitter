from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from micro_twitter.common.models import BaseModel


class Tweet(BaseModel, models.Model):
    public_id = ShortUUIDField(
        length=22,
        max_length=22,
        alphabet="123456789",
    )
    content = models.CharField(
        verbose_name=_("content"),
        max_length=140,
    )
    author = models.ForeignKey(
        verbose_name=_("author"),
        to=settings.AUTH_USER_MODEL,
        related_name="tweets",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.public_id
