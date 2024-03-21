from django.contrib import admin

from resource_assigner.models import AssigmentRule, AssignmentConstraint, TaskResourceAssigment


@admin.register(AssignmentConstraint)
class AssignmentConstraint(admin.ModelAdmin):
    list_display = [
        "task",
        "resource_pool",
        "required_units",
        "created_at",
        "created_by",
    ]
    list_filter = [
        "task",
        "resource_pool",
        "resources",
        "work_units",
        "created_at",
        "created_by",
    ]
    search_fields = ["task", "resource_pool"]


@admin.register(AssigmentRule)
class AssigmentRule(admin.ModelAdmin):
    list_display = [
        "name",
        "work_center",
        "created_at",
        "created_by",
    ]
    list_filter = ["work_center", "created_at", "created_by"]
    search_fields = ["name"]


@admin.register(TaskResourceAssigment)
class TaskResourceAssigment(admin.ModelAdmin):
    list_display = [
        "task",
        "resource_count",
        "use_all_resources",
        "created_at",
        "created_by",
    ]
    list_filter = [
        "task",
        "created_at",
        "created_by",
    ]
    search_fields = ["task", "resource_pool"]

