from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import (
    EmailCheckSerializer,
    LoginSerializer,
    RegistrationSerializer,
    get_user_fullname,
)


class RegistrationView(APIView):
    """Create an account and return its token and user details."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
            "fullname": get_user_fullname(user),
            "email": user.email,
            "user_id": user.id,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Authenticate an account and return its token and user details."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
            "fullname": get_user_fullname(user),
            "email": user.email,
            "user_id": user.id,
        }
        return Response(data, status=status.HTTP_200_OK)


class EmailCheckView(APIView):
    """Let authenticated users find user details by email address."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = EmailCheckSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        data = self.get_user_data(user)
        return Response(data, status=status.HTTP_200_OK)

    def get_user_data(self, user):
        return {
            "id": user.id,
            "email": user.email,
            "fullname": get_user_fullname(user),
        }
