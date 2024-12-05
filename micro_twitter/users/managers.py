from django.contrib.auth.models import UserManager as DjangoUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(DjangoUserManager):
    """Custom manager for :model:'users.User' model."""

    use_in_migrations = True

    def get_by_natural_key(self, username):
        """Allow authentication by case-insensitive emails."""
        return self.get(**{"{}__iexact".format(self.model.USERNAME_FIELD): username})

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set."))

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)
