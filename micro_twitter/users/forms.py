"""Users App Forms."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

User = get_user_model()


class UserChangeForm(DjangoUserChangeForm):
    """
    Subclass of django.contrib.auth.forms.UserChangeForm.
    """

    class Meta:
        model = User
        exclude = [
            "following",
            "date_joined",
        ]

    def clean_username(self):
        """Validate username doesn't exist, including different case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("User with this username already exists.")
        return username

    def clean_email(self):
        """Validate email doesn't exists, including different case."""
        email = self.cleaned_data["email"]
        if (
            email
            and self._meta.model.objects.filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("User with this email already exists.")
        return email


class UserCreationForm(DjangoUserCreationForm):
    """
    Subclass of django.contrib.auth.forms.UserCreationForm.
    """

    class Meta:
        model = User
        exclude = [
            "following",
            "date_joined",
        ]

    def clean_username(self):
        """Validate username doesn't exist, including different case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            raise forms.ValidationError("User with this username already exists.")
        return username

    def clean_email(self):
        """Validate email doesn't exists, including different case."""
        email = self.cleaned_data["email"]
        if email and self._meta.model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("User with this email already exists.")
        return email
