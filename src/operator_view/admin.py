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
        "tag_list",
        "thumbnail",
        "created_at",
        "created_by",
    ]
    list_filter = ("issuer", "created_at", "created_by")
    search_fields = ["name"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])


@admin.register(OperatorViewTask)
class OperatorViewTask(admin.ModelAdmin):
    list_display = [
        "name",
        "item",
        "assigned_resources",
        "planned_start_datetime",
        "thumbnail_url",
        "created_at",
        "created_by",
    ]
    list_filter = ("created_at", "created_by")
    search_fields = ["name"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("assigned_resources")

    def assigned_resources(self, obj):
        return ", ".join([p for p in obj.assigned_resources.all()])


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
