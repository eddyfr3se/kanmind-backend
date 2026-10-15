from uuid import uuid4

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.models import UserProfile


def get_user_fullname(user):
    """Return the profile name or a Django name for users without a profile."""
    try:
        return user.profile.fullname
    except UserProfile.DoesNotExist:
        return user.get_full_name() or user.username


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration data and create a user and full-name profile."""

    fullname = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    repeated_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = [
            "fullname",
            "email",
            "password",
            "repeated_password",
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        fullname = validated_data.pop("fullname")
        validated_data.pop("repeated_password")
        user = User.objects.create_user(
            username=str(uuid4()),
            email=validated_data["email"],
            password=validated_data["password"],
        )
        UserProfile.objects.create(
            user=user,
            fullname=fullname,
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Validate email and password and authenticate the matching account."""

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        account = User.objects.filter(email__iexact=attrs["email"]).first()
        if account is None:
            raise serializers.ValidationError("Invalid email or password.")
        user = authenticate(
            username=account.username,
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs


class EmailCheckSerializer(serializers.Serializer):
    """Validate the email query parameter used for user lookup."""

    email = serializers.EmailField()
