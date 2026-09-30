"""User information required by the KanMind API."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Keep Django authentication and add the API account fields."""

    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(unique=True)
    fullname = models.TextField()

    def __str__(self):
        return self.fullname or self.username
