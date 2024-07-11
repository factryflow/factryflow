from django.contrib import admin

from resource_assigner.models import (
    AssigmentRule,
    AssignmentConstraint,
    TaskResourceAssigment,
    TaskRuleAssignment,
)


@admin.register(AssignmentConstraint)
class AssignmentConstraint(admin.ModelAdmin):
    list_display = [
        "task",
        "resource_group",
        "created_at",
        "created_by",
    ]
    list_filter = [
        "task",
        "resource_group",
        "resources",
        "created_at",
        "created_by",
    ]
    search_fields = ["task", "resource_group"]


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
        "created_at",
        "created_by",
    ]
    list_filter = [
        "task",
        "created_at",
        "created_by",
    ]
    search_fields = ["task"]


@admin.register(TaskRuleAssignment)
class TaskRuleAssignment(admin.ModelAdmin):
    list_display = ["task", "assigment_rule", "is_applied"]
    list_filter = ["is_applied"]
