from django.contrib import admin

from resource_manager.models import Resource, ResourcePool


@admin.register(Resource)
class Resource(admin.ModelAdmin):
    list_display = ["name", "created_at", "created_by"]
    list_filter = ["created_at", "created_by"]
    search_fields = ["name"]


@admin.register(ResourcePool)
class ResourcePool(admin.ModelAdmin):
    list_display = ["name", "external_id", "created_at", "created_by"]
    list_filter = ["created_at", "created_by"]
    search_fields = ["name"]
