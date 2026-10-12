from rest_framework.permissions import BasePermission


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
