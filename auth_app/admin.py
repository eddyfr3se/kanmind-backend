"""Manage users with Django's existing password and permission forms."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AccountAdmin(UserAdmin):
    """Include the API name in user creation and editing."""

    list_display = ("username", "email", "fullname", "is_staff")
    search_fields = ("username", "email", "fullname")
    fieldsets = UserAdmin.fieldsets + (("KanMind", {"fields": ("fullname",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("KanMind", {"fields": ("email", "fullname")}),
    )
