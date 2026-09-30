"""Public registration endpoint."""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AccountResponseSerializer, RegistrationSerializer


class RegistrationView(APIView):
    """Register an account without requiring an existing token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Return the newly registered account with HTTP 201."""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = AccountResponseSerializer(user)
        return Response(response.data, status=status.HTTP_201_CREATED)
