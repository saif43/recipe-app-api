from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOEKN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        payload = {
            "email": "test@email.com",
            "password": "testpass",
            "name": "testname",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_if_user_exists(self):
        """Test if the user is already created"""

        payload = {
            "email": "test@email.com",
            "password": "testpass",
            "name": "testname",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_password_short(self):
        """check if the user has short password"""

        payload = {
            "email": "test@email.com",
            "password": "test",
            "name": "testname",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token(self):
        """test 1"""
        payload = {"email": "test@gmail.com", "password": "testpass"}
        create_user(**payload)

        res = self.client.post(TOEKN_URL, payload)

        self.assertIn("token", res.data)

        """test 2"""
        payload = {"email": "test2@gmail.com", "password": "test2pass"}
        create_user(**payload)

        res = self.client.post(TOEKN_URL, {"email": "test@gmail.com"})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the users API (private)"""

    def setUp(self):
        self.user = create_user(
            email="test@gmail.com", password="testpass", name="name"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """Test retriving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email,})

    def test_post_method_not_allowed(self):
        """Test method not allowed"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test update user profile"""
        payload = {"password": "testpass1234", "name": "test name"}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
