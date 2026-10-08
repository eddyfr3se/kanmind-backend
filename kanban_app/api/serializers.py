from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board, Task


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title", "members"]


class BoardListSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    # Board task counters are implemented in a later project stage.
    ticket_count = serializers.IntegerField(read_only=True, default=0)
    tasks_to_do_count = serializers.IntegerField(read_only=True, default=0)
    tasks_high_prio_count = serializers.IntegerField(read_only=True, default=0)
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]

    def get_member_count(self, obj):
        return obj.members.count()


class BoardMemberSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(
        source="profile.fullname",
        read_only=True,
    )

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskSerializer(serializers.ModelSerializer):
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    # Comments are implemented in a later project stage.
    comments_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee",
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        ]

    def validate(self, attrs):
        board = attrs["board"]
        for field in ["assignee", "reviewer"]:
            user = attrs.get(field)
            if user and not board.members.filter(id=user.id).exists():
                raise serializers.ValidationError({
                    f"{field}_id": "User must be a member of the board."
                })
        return attrs


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    owner_data = BoardMemberSerializer(source="owner", read_only=True)
    members_data = BoardMemberSerializer(
        source="members",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data"]
