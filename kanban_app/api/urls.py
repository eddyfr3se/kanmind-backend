from django.urls import path

from kanban_app.api.views import BoardDetailView, BoardListCreateView


urlpatterns = [
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
