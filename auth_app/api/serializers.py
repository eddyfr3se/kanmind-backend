from uuid import uuid4

from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
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
