from django.urls import path

from kanban_app.api.views import (
    AssignedTaskListView,
    BoardDetailView,
    BoardListCreateView,
    ReviewingTaskListView,
    TaskCreateView,
    TaskUpdateDeleteView,
)


urlpatterns = [
    path(
        "tasks/assigned-to-me/",
        AssignedTaskListView.as_view(),
        name="tasks-assigned-to-me",
    ),
    path(
        "tasks/reviewing/",
        ReviewingTaskListView.as_view(),
        name="tasks-reviewing",
    ),
    path("tasks/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/",
        TaskUpdateDeleteView.as_view(),
        name="task-update-delete",
    ),
    path(
        "boards/",
        BoardListCreateView.as_view(),
        name="board-list-create",
    ),
    path(
        "boards/<int:pk>/",
        BoardDetailView.as_view(),
        name="board-detail",
    ),
]
