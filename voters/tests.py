import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITransactionTestCase, APIClient

from voters.models import Voter


def create_sample_voter(**params):
    """Create and return a sample voter"""
    defaults = {
        "voter": get_user_model().objects.create_user(
            "user1@kts.com", "testpass"
        ),
    }
    defaults.update(params)

    return Voter.objects.create(**defaults)


class ImageUploadTest(APITransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@kts.com", "testpass"
        )
        self.client.force_authenticate(self.user)
        self.voter = create_sample_voter()

    def tearDown(self):
        Voter.objects.all().delete()
        super().tearDown()

    def test_upload_image_to_voter(self):
        url = reverse("voters:voters-list")
        # , kwargs={"pk": self.voter.pk})
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url, {"picture": ntf, "voter": self.user.id}, format="multipart"
            )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("picture", res.data)
        self.assertTrue(Voter.objects.filter(id=res.data.get("id")).exists())
        voter = Voter.objects.get(id=res.data.get("id"))
        self.assertTrue(os.path.exists(voter.picture.path))

    def test_cleanup_after_delete(self):
        url = reverse("voters:voters-list")
        # , kwargs={"pk": self.voter.pk})
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url, {"picture": ntf, "voter": self.user.id}, format="multipart"
            )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("picture", res.data)
        self.assertTrue(Voter.objects.filter(id=res.data.get("id")).exists())
        voter = Voter.objects.get(id=res.data.get("id"))
        picture_path = voter.picture.path
        url = reverse("voters:voters-detail", kwargs={"pk": voter.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(os.path.exists(picture_path))
