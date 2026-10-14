from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from kanban_app.models import Task


class IsBoardOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.owner_id == request.user.id
        if request.method == "DELETE":
            return is_owner
        is_member = obj.members.filter(
            id=request.user.id,
        ).exists()
        return is_owner or is_member


class CanEditOrDeleteTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            is_creator = obj.creator_id == request.user.id
            is_board_owner = obj.board.owner_id == request.user.id
            return is_creator or is_board_owner
        if request.method == "PATCH":
            return obj.board.members.filter(id=request.user.id).exists()
        return False


class IsTaskBoardMember(BasePermission):
    message = "You must be a member of the board."

    def has_permission(self, request, view):
        task = get_object_or_404(Task, pk=view.kwargs["task_id"])
        return task.board.members.filter(id=request.user.id).exists()


class IsCommentAuthor(BasePermission):
    message = "Only the comment author can delete this comment."

    def has_object_permission(self, request, view, obj):
        return obj.author_id == request.user.id
