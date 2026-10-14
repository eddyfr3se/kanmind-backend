from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Store the full name associated with a Django user account."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    fullname = models.TextField()

    def __str__(self):
        return self.fullname
