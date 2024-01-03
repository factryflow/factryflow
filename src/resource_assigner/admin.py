from django.contrib import admin
from resource_assigner.models import AssigmentRule, TaskResourceAssigment


@admin.register(TaskResourceAssigment)
class TaskResourceAssigment(admin.ModelAdmin):
    list_display = [
        "task",
        "resource_group",
        "resource_count",
        "use_all_resources",
        "created_at",
        "created_by",
    ]
    list_filter = ["task", "resource_group", "created_at", "created_by"]
    search_fields = ["task", "resource_group"]

@admin.register(AssigmentRule)
class AssigmentRule(admin.ModelAdmin):
    list_display = [
        "name",
        "resource_group",
        "work_center",
        "created_at",
        "created_by",
    ]
    list_filter = ["resource_group", "work_center", "created_at", "created_by"]
    search_fields = ["name"]
