from django.contrib import admin
from .models import CustomField, NestedCriteriaGroup, NestedCriteria


@admin.register(CustomField)
class CustomField(admin.ModelAdmin):
    list_display = [
        "name",
        "label",
        "content_type",
        "field_type",
        "created_at",
        "created_by",
    ]
    list_filter = ["field_type", "created_at", "created_by"]
    search_fields = ["name", "label"]


@admin.register(NestedCriteriaGroup)
class NestedCriteriaGroup(admin.ModelAdmin):
    list_display = ["operator", "created_at", "created_by"]
    list_filter = ["operator", "created_at", "created_by"]
    search_fields = ["operator"]


@admin.register(NestedCriteria)
class NestedCriteria(admin.ModelAdmin):
    list_display = ["group", "content_type", "object_id"]
    list_filter = ["group", "content_type", "object_id"]
    search_fields = ["group", "content_type", "object_id"]
