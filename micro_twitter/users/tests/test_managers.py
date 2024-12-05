from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CustomUserModelTest(TestCase):
    EMAIL = "email@gmail.com"
    USERNAME = "username123"
    PASSWORD = "password123"

    def test_create_user_successful(self):
        user = User.objects.create_user(
            email=self.EMAIL, username=self.USERNAME, password=self.PASSWORD
        )

        self.assertEqual(user.email, self.EMAIL)
        self.assertEqual(user.username, self.USERNAME)
        self.assertTrue(user.check_password(self.PASSWORD))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_empty_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username=self.USERNAME, email=None, password=self.PASSWORD
            )

    def test_create_superuser_sucessful(self):
        superuser = User.objects.create_superuser(
            email=self.EMAIL, password=self.PASSWORD
        )

        self.assertEqual(superuser.email, self.EMAIL)
        self.assertTrue(superuser.check_password(self.PASSWORD))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_empty_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=None, password=self.PASSWORD)

    def test_create_superuser_non_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.EMAIL, password=self.PASSWORD, is_staff=False
            )

    def test_create_superuser_non_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.EMAIL, password=self.PASSWORD, is_superuser=False
            )

    def test_get_by_natural_key_case_insensitive(self):
        user = User.objects.create_user(
            email=self.EMAIL, username=self.USERNAME, password=self.PASSWORD
        )
        retrieved_user = User.objects.get_by_natural_key("Email@gmail.com")
        self.assertEqual(user, retrieved_user)

    def test_get_by_natural_key_user_does_not_exist(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get_by_natural_key("nonexistent@example.com")
