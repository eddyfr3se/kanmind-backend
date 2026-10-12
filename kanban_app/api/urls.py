from django.urls import path

from kanban_app.api.views import (
    BoardDetailView,
    BoardListCreateView,
    TaskCreateView,
    TaskUpdateDeleteView,
)


urlpatterns = [
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
