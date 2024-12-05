import pathlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from micro_twitter.common.models import BaseModel
from micro_twitter.users.managers import UserManager


def user_profile_picture_upload_handler(instance, filename):
    return f"profile_pictures/{uuid.uuid1()}{pathlib.Path(filename).suffix}"


class User(BaseModel, AbstractUser):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
    )
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text=_("50 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
    )
    profile_picture = models.ImageField(
        verbose_name=_("profile picture"),
        upload_to=user_profile_picture_upload_handler,
        null=True,
        blank=True,
    )
    following = models.ManyToManyField(
        verbose_name=_("following"),
        to="self",
        related_name="followers",
        related_query_name="followed_by",
        symmetrical=False,
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
