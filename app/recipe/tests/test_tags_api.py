from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")


class PublicTagsApiTests(TestCase):
    """Test the public API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retriving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the private API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com", name="Test name", password="testpass"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """Test retriving tags"""

        Tag.objects.create(user=self.user, name="Vagan")
        Tag.objects.create(user=self.user, name="Pizza")

        tags = Tag.objects.all().order_by("-name")

        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_authenticated_tag(self):
        """test tags by authenticated user"""

        Tag.objects.create(user=self.user, name="Vagan")
        Tag.objects.create(user=self.user, name="Pizza")

        user2 = get_user_model().objects.create(
            email="test2@gmail.com", name="Test2 name", password="test2pass"
        )

        Tag.objects.create(user=user2, name="Coffee")

        res = self.client.get(TAGS_URL)

        self.assertEqual(len(res.data), 2)

    def test_create_tag_successful(self):
        """Test creating a new tag"""

        payload = {"name": "Something"}

        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(user=self.user, name=payload["name"]).exists()

        self.assertTrue(exists)

    def test_tag_create_invalid(self):
        """Test if tag has enough length"""

        payload = {"name": ""}

        self.client.post(TAGS_URL, payload)

        res = self.client.post(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

