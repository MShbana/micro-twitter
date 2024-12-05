from io import BytesIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword",
        )
        self.target_user = User.objects.create_user(
            username="targetuser",
            email="target@example.com",
            password="securepassword",
        )

    @mock.patch("micro_twitter.users.views.send_email")
    def test_register_user(self, mock_send_email):
        url = reverse("users:user-register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123!",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], data["username"])
        mock_send_email.apply_async.assert_called_once()

    @mock.patch("micro_twitter.users.views.send_email")
    def test_register_user_with_profile_picture(self, mock_send_email):
        picture_data = BytesIO()
        picture = Image.new("RGB", (100, 100), "white")
        picture.save(picture_data, format="png")
        picture_data.seek(0)

        url = reverse("users:user-register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "profile_picture": SimpleUploadedFile(
                "test.png", picture_data.read(), content_type="image/png"
            ),
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], data["username"])
        mock_send_email.apply_async.assert_called_once()

    @mock.patch("micro_twitter.users.views.send_email")
    def test_register_user_with_wrong_profile_picture_format(self, mock_send_email):
        # https://stackoverflow.com/a/75754174
        picture_data = BytesIO()
        picture = Image.new("RGB", (100, 100), "white")
        picture.save(picture_data, format="gif")
        picture_data.seek(0)

        url = reverse("users:user-register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "profile_picture": SimpleUploadedFile(
                "test.png", picture_data.read(), content_type="image/gif"
            ),
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("profile_picture", response.data)
        mock_send_email.assert_not_called()

    @mock.patch("micro_twitter.users.views.send_email")
    def test_register_user_duplicate_email(self, mock_send_email):
        url = reverse("users:user-register")
        data = {
            "username": "anotheruser",
            "email": "test@example.com",
            "password": "AnotherPassword123!",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        mock_send_email.assert_not_called()

    def test_login_user(self):
        url = reverse("users:user-login")
        data = {
            "email": "test@example.com",
            "password": "securepassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_follow_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-follow")
        data = {
            "target_username": self.target_user.username,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)
        self.assertTrue(
            self.user.following.filter(username=self.target_user.username).exists()
        )

    def test_follow_user_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-follow")
        data = {
            "target_username": self.user.username,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "You cannot follow your own account.")

    def test_follow_user_already_followed(self):
        self.client.force_authenticate(user=self.user)
        self.user.following.add(self.target_user)
        url = reverse("users:user-follow")
        data = {
            "target_username": self.target_user.username,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            f"Successfully followed {self.target_user.username}.",
        )
