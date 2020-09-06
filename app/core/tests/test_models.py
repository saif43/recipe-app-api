from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@email.com", password="testpass"):
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(user=sample_user(), name="Vegan")

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(user=sample_user(), name="Vegan")

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = models.Recipe(
            user=sample_user(), title="Hot soup", time_minutes=5, price=6.23
        )

        self.assertEqual(str(recipe), recipe.title)