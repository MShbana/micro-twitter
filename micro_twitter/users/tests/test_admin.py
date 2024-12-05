from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

from micro_twitter.users.admin import UserAdmin
from micro_twitter.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class MockRequest:
    "Mock request to be passed for methods that require a request."


class UserAdminTests(TestCase):
    MOCK_PASSWORD = "3h1G1(Wf"

    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(User, self.site)
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=self.MOCK_PASSWORD,
        )
        self.other_user = User.objects.create_user(
            username="follower",
            email="follower@example.com",
            password=self.MOCK_PASSWORD,
        )
        self.user.followers.add(self.other_user)

    def test_form_initialization(self):
        """Test that the correct forms are used in the admin."""
        self.assertEqual(self.user_admin.form, UserChangeForm)
        self.assertEqual(self.user_admin.add_form, UserCreationForm)

    def test_list_display(self):
        """Test the list_display fields in admin."""
        self.assertIn("email", self.user_admin.list_display)
        self.assertIn("username", self.user_admin.list_display)

    def test_add_user(self):
        """Test adding a user via the admin."""
        form_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": self.MOCK_PASSWORD,
            "password1": self.MOCK_PASSWORD,
            "password2": self.MOCK_PASSWORD,
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_edit_user(self):
        """Test editing a user via the admin."""
        form_data = {
            "email": "updated@example.com",
            "username": "updateduser",
        }
        form = UserChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")

    def test_readonly_fields(self):
        """Test that readonly fields are properly handled."""
        readonly_fields = self.user_admin.get_readonly_fields(MockRequest(), self.user)
        self.assertIn("last_login", readonly_fields)
        self.assertIn("date_joined", readonly_fields)

    def test_get_followers(self):
        """Test the get_followers method."""
        followers = self.user_admin.get_followers(self.user)
        self.assertEqual(followers, "follower@example.com")

    def test_get_followers_no_followers(self):
        """Test get_followers when the user has no followers."""
        # Ensure the user has no followers.
        self.user.followers.clear()
        followers = self.user_admin.get_followers(self.user)
        self.assertEqual(followers, "")

    def test_get_followers_with_followers(self):
        """Test get_followers when the user has followers."""
        # Ensure the user has one follower.
        followers = self.user_admin.get_followers(self.user)
        self.assertEqual(followers, "follower@example.com")

    def test_get_followers_multiple_followers(self):
        """Test get_followers when the user has multiple followers."""
        # Add another follower.
        another_follower = User.objects.create_user(
            username="anotherfollower",
            email="anotherfollower@example.com",
            password=self.MOCK_PASSWORD,
        )
        self.user.followers.add(another_follower)

        followers = self.user_admin.get_followers(self.user)
        self.assertEqual(
            followers,
            "follower@example.com, anotherfollower@example.com",
        )
