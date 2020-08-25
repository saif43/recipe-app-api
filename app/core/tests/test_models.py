from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_userCreateWithEmailAndPassword(self):
        """Testing user creation"""
        email = "test@gmail.com"
        password = "test123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_has_valid_email(self):
        """Testing if user has valid email address"""
        email = "test@GMAIL.com"
        password = "test123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email.lower())

    def test_user_has_email(self):
        """Test if the user has email address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_new_created_superuser(self):
        """Test if the superuser is created"""

        email = "test@gmail.com"
        password = "test123"

        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
