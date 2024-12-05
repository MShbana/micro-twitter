from django.contrib.auth import get_user_model
from django.test import TestCase

from micro_twitter.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserFormsTests(TestCase):
    MOCK_PASSWORD = "3h1G1(Wf"

    def setUp(self):
        # Create an initial user for testing.
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=self.MOCK_PASSWORD,
        )

    def test_user_creation_form_valid(self):
        """Test that UserCreationForm is valid with unique username and email."""
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": self.MOCK_PASSWORD,
            "password1": self.MOCK_PASSWORD,
            "password2": self.MOCK_PASSWORD,
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_invalid_username(self):
        """Test that UserCreationForm raises a validation error if the username already exists."""
        form_data = {
            "username": "testuser",
            "email": "newuser@example.com",
            "password1": self.MOCK_PASSWORD,
            "password2": self.MOCK_PASSWORD,
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["username"], ["User with this username already exists."]
        )

    def test_user_creation_form_invalid_email(self):
        """Test that UserCreationForm raises a validation error if the email already exists."""
        form_data = {
            "username": "newuser",
            "email": "testuser@example.com",
            "password1": self.MOCK_PASSWORD,
            "password2": self.MOCK_PASSWORD,
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["User with this email already exists."])

    def test_user_change_form_valid(self):
        """Test that UserChangeForm is valid when updating with unique username and email."""

        form_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "password": self.MOCK_PASSWORD,
        }
        form = UserChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_change_form_invalid_username(self):
        """Test that UserChangeForm raises a validation error if the username already exists."""
        new_user = User.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password=self.MOCK_PASSWORD,
        )
        form_data = {
            "username": "testuser",
            "email": "updateduser@example.com",
            "password": self.MOCK_PASSWORD,
        }
        form = UserChangeForm(instance=new_user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["username"], ["User with this username already exists."]
        )

    def test_user_change_form_invalid_email(self):
        """Test that UserChangeForm raises a validation error if the email already exists."""
        new_user = User.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password=self.MOCK_PASSWORD,
        )
        form_data = {
            "username": "updateduser",
            "email": "testuser@example.com",
            "password": self.MOCK_PASSWORD,
        }
        form = UserChangeForm(instance=new_user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["User with this email already exists."])
