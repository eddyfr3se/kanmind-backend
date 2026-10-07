from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title", "members"]


class BoardListSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    # Task counts stay zero until the Task model is implemented.
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


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)
    members = BoardMemberSerializer(many=True, read_only=True)
    # Actual tasks will be included when the Task model is implemented.
    tasks = serializers.ListField(read_only=True, default=list)

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
