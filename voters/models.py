from django.db import models
from django.contrib.auth import get_user_model


class Voter(models.Model):
    voter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    picture = models.FileField(null=True, upload_to="media/")
