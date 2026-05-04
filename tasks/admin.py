from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "priority", "due_date", "created_at")
    list_filter = ("status", "priority", "is_archived")
    search_fields = ("title", "description", "user__username")