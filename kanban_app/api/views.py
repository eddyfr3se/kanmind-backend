from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kanban_app.api.permissions import (
    CanEditOrDeleteTask,
    IsBoardOwnerOrMember,
    IsCommentAuthor,
    IsTaskBoardMember,
)
from kanban_app.api.serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardListSerializer,
    BoardUpdateResponseSerializer,
    CommentSerializer,
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateResponseSerializer,
    TaskUpdateSerializer,
)
from kanban_app.models import Board, Comment, Task


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


class AssignedTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class ReviewingTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_board(self):
        board_id = serializers.IntegerField(min_value=1).run_validation(
            self.request.data.get("board")
        )
        return get_object_or_404(Board, pk=board_id)

    def create(self, request, *args, **kwargs):
        board = self.get_board()
        if not board.members.filter(id=request.user.id).exists():
            raise PermissionDenied("You must be a member of the board.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(creator=request.user)
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED,
        )


class TaskUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditOrDeleteTask]
    http_method_names = ["patch", "delete", "options"]

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(
            task, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_serializer = TaskUpdateResponseSerializer(task)
        return Response(response_serializer.data)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsTaskBoardMember]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return Comment.objects.filter(
            task_id=self.kwargs["task_id"],
        ).order_by("created_at", "id")

    def perform_create(self, serializer):
        serializer.save(
            task_id=self.kwargs["task_id"],
            author=self.request.user,
        )


class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    http_method_names = ["delete", "options"]
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        task = get_object_or_404(Task, pk=self.kwargs["task_id"])
        return Comment.objects.filter(task=task)
