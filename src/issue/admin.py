from django.contrib import admin

from .models import Issue


@admin.register(Issue)
class Issue(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "status",
        "thumbnail",
        "tag_list",
        "created_at",
        "created_by",
    ]
    list_filter = ("created_at", "created_by")
    search_fields = ["name"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join([o.name for o in obj.tags.all()])
