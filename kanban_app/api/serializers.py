from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board, Comment, Task


class BoardCreateSerializer(serializers.ModelSerializer):
    """Validate titles and member lists for board creation and updates."""

    class Meta:
        model = Board
        fields = ["title", "members"]


class BoardListSerializer(serializers.ModelSerializer):
    """Return board summaries with membership and task counts."""

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
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

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()


class BoardMemberSerializer(serializers.ModelSerializer):
    """Return user IDs, emails and full names for nested API responses."""

    fullname = serializers.CharField(
        source="profile.fullname",
        read_only=True,
    )

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskSerializer(serializers.ModelSerializer):
    """Return task details with assigned users and the comment count."""

    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

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

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskCreateSerializer(serializers.ModelSerializer):
    """Validate task input and require assigned users to be board members."""

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


class TaskUpdateSerializer(TaskCreateSerializer):
    """Validate partial task updates while preserving the existing board."""

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        ]

    def validate(self, attrs):
        self.validate_board_reference()
        board = self.instance.board
        for field in ["assignee", "reviewer"]:
            user = attrs.get(field)
            if user and not board.members.filter(id=user.id).exists():
                raise serializers.ValidationError({
                    f"{field}_id": "User must be a member of the board."
                })
        return attrs

    def validate_board_reference(self):
        board_id = self.initial_data.get("board", self.instance.board_id)
        if str(board_id) != str(self.instance.board_id):
            raise serializers.ValidationError({
                "board": "The board cannot be changed."
            })


class TaskUpdateResponseSerializer(TaskSerializer):
    """Return the documented task fields after a partial update."""

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
        ]


class BoardTaskSerializer(TaskSerializer):
    """Return nested task details without repeating the enclosing board ID."""

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]


class BoardDetailSerializer(serializers.ModelSerializer):
    """Return a board with its members and tasks."""

    owner_id = serializers.IntegerField(read_only=True)
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = BoardTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    """Return owner and member details after a board update."""

    owner_data = BoardMemberSerializer(source="owner", read_only=True)
    members_data = BoardMemberSerializer(
        source="members",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data"]


class CommentSerializer(serializers.ModelSerializer):
    """Accept comment content and return its author and creation time."""

    author = serializers.CharField(
        source="author.profile.fullname",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]
        read_only_fields = ["id", "created_at"]
