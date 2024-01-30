from django.contrib import admin

from .models import Comment, Issue


@admin.register(Issue)
class Issue(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "status",
        "thumbnail",
        "task",
        "tag_list",
        "created_at",
        "created_by",
    ]
    list_filter = ("created_at", "created_by")
    search_fields = ["title"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join([o.name for o in obj.tags.all()])


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ["body", "issue", "created_at", "created_by", "updated_by"]
    list_filter = ("created_at", "created_by")
    search_fields = ["created_by"]
