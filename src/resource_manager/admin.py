from django.contrib import admin

from resource_manager.models import Resource, ResourcePool, WorkUnit


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "created_by"]
    list_filter = ["created_at", "created_by"]
    search_fields = ["name"]


@admin.register(ResourcePool)
class ResourcePoolAdmin(admin.ModelAdmin):
    list_display = ["name", "external_id", "created_at", "created_by"]
    list_filter = ["created_at", "created_by"]
    search_fields = ["name"]


@admin.register(WorkUnit)
class WorkUnitAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "created_by"]
    list_filter = ["created_at", "created_by"]
    search_fields = ["name"]
