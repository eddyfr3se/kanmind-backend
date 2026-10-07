from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kanban_app.api.permissions import IsBoardOwnerOrMember
from kanban_app.api.serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardListSerializer,
    BoardUpdateResponseSerializer,
)
from kanban_app.models import Board


class BoardListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BoardCreateSerializer
        return BoardListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)
        response_serializer = BoardListSerializer(board)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    http_method_names = ["get", "patch", "delete", "head", "options"]
    permission_classes = [
        IsAuthenticated,
        IsBoardOwnerOrMember,
    ]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return BoardCreateSerializer
        return BoardDetailSerializer

    def update(self, request, *args, **kwargs):
        board = self.get_object()
        serializer = self.get_serializer(
            board, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_serializer = BoardUpdateResponseSerializer(board)
        return Response(response_serializer.data)
