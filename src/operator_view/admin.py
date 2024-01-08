from django.contrib import admin

from .models.exception import OperatorViewException
from .models.issue import Issue
from .models.task import OperatorViewTask


@admin.register(Issue)
class Issue(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "issuer",
        "thumbnail",
        "created_at",
        "created_by",
    ]
    list_filter = ("issuer", "created_at", "created_by")
    search_fields = ["name"]


@admin.register(OperatorViewTask)
class OperatorViewTask(admin.ModelAdmin):
    list_display = [
        "name",
        "item",
        "assigned_resource",
        "planned_start_datetime",
        "thumbnail_url",
        "created_at",
        "created_by",
    ]
    list_filter = ("created_at", "created_by")
    search_fields = ["name"]


@admin.register(OperatorViewException)
class OperatorViewException(admin.ModelAdmin):
    list_display = [
        "external_id",
        "operational_exception_type",
        "item",
        "task",
        "resource",
        "created_at",
        "created_by",
    ]
    list_filter = ("created_at", "created_by")
    search_fields = ["name"]
