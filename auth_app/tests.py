"""Check persistence and security properties of registration."""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from auth_app.api.serializers import RegistrationSerializer

User = get_user_model()


class RegistrationTests(TestCase):
    """Use an isolated database for account creation checks."""

    def setUp(self):
        self.client = APIClient()
        self.data = {
            "fullname": "Ada Example",
            "email": "ada@example.com",
            "password": "  Practice-password-71!  ",
            "repeated_password": "  Practice-password-71!  ",
        }

    def register(self, **changes):
        """Submit registration data with optional replacements."""
        return self.client.post(
            "/api/registration/", {**self.data, **changes}, format="json",
        )

    def test_password_is_hashed_without_trimming(self):
        response = self.register()
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(email=self.data["email"])
        self.assertNotEqual(user.password, self.data["password"])
        self.assertTrue(user.check_password(self.data["password"]))
        self.assertFalse(user.check_password(self.data["password"].strip()))
        self.assertEqual(
            Token.objects.get(user=user).key, response.data["token"],
        )
        self.assertEqual(set(response.data), {
            "token", "fullname", "email", "user_id",
        })

    def test_duplicate_email_does_not_create_another_user(self):
        self.register()
        response = self.register(email="ADA@EXAMPLE.COM")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)

    def test_invalid_data_does_not_create_user_or_token(self):
        for changes in ({"email": "invalid"}, {"repeated_password": "other"}):
            with self.subTest(changes=changes):
                self.assertEqual(self.register(**changes).status_code, 400)
                self.assertEqual(User.objects.count(), 0)
                self.assertEqual(Token.objects.count(), 0)

    def test_client_cannot_grant_admin_permissions(self):
        response = self.register(is_staff=True, is_superuser=True, groups=[1])
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=response.data["user_id"])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.groups.exists())

    def test_failed_token_creation_rolls_back_user(self):
        serializer = RegistrationSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        with patch.object(Token.objects, "create", side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                serializer.save()
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Token.objects.count(), 0)

    def test_duplicate_between_validation_and_save_returns_field_error(self):
        serializer = RegistrationSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        self.register()
        with self.assertRaises(ValidationError) as error:
            serializer.save()
        self.assertIn("email", error.exception.detail)
        self.assertEqual(User.objects.count(), 1)

    def test_admin_can_open_account_forms(self):
        admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="test-only",
        )
        self.client.force_login(admin)
        for url in ("/admin/auth_app/user/add/", "/admin/auth_app/user/"):
            self.assertEqual(self.client.get(url).status_code, 200)
