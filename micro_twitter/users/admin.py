from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from micro_twitter.users.forms import UserChangeForm, UserCreationForm


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin):
    """ModelAdmin for User Model."""

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "profile_picture",
                )
            },
        ),
        (
            _("Relationships"),
            {
                "fields": (
                    "following",
                    "get_followers",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "username",
                    "password1",
                    "password2",
                ]
            },
        ),
    ]
    readonly_fields = [
        "last_login",
        "date_joined",
        "following",
        "get_followers",
    ]
    ordering = [
        "-time_created",
    ]

    @admin.display(description="Followers")
    def get_followers(self, obj):
        followers = obj.followers.only("email")
        if not followers.exists():
            return ""

        return ", ".join([follower.email for follower in followers])
