"""Validate registration data and create accounts."""
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Accept only the four fields required for registration."""

    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    repeated_password = serializers.CharField(
        write_only=True, trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = ("fullname", "email", "password", "repeated_password")

    def validate_email(self, value):
        """Treat email addresses as case-insensitive account identifiers."""
        value = value.lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, attrs):
        """Reject differing passwords before writing any account data."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({
                "repeated_password": "Passwords do not match.",
            })
        return attrs

    def create(self, validated_data):
        """Handle duplicate accounts that appear after validation."""
        validated_data.pop("repeated_password")
        try:
            return self.create_account(validated_data)
        except IntegrityError:
            email = validated_data["email"]
            if not User.objects.filter(username=email).exists():
                raise
            raise serializers.ValidationError({
                "email": "An account with this email already exists.",
            })

    @transaction.atomic
    def create_account(self, validated_data):
        """Save the password through Django and create the associated token."""
        user = User.objects.create_user(
            username=validated_data["email"], **validated_data,
        )
        Token.objects.create(user=user)
        return user


class AccountResponseSerializer(serializers.ModelSerializer):
    """Return the public account fields and its authentication token."""

    token = serializers.CharField(source="auth_token.key", read_only=True)
    user_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = User
        fields = ("token", "fullname", "email", "user_id")
        read_only_fields = fields
