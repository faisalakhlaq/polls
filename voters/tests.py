import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from voters.models import Voter


def create_sample_voter(**params):
    """Create and return a sample recipe"""
    defaults = {
        "voter": get_user_model().objects.create_user(
            "user1@kts.com", "testpass"
        ),
    }
    defaults.update(params)

    return Voter.objects.create(**defaults)


class ImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@kts.com", "testpass"
        )
        self.client.force_authenticate(self.user)
        self.voter = create_sample_voter()

    def tearDown(self):
        self.voter.picture.delete()
        super().tearDown()

    def test_upload_image_to_recipe(self):
        """Test uploading an email to recipe"""
        url = reverse("voters:voters:-list", kwargs={"pk": self.voter.pk})
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"picture": ntf}, format="multipart")

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("picture", res.data)
        self.assertTrue(os.path.exists(self.recipe.picture.path))
