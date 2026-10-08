from django.contrib import admin

from kanban_app.models import Board, Task


admin.site.register(Board)
admin.site.register(Task)
