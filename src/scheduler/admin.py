from django.contrib import admin

# Register your models here.
from .models import ResourceAllocations, ResourceIntervals, SchedulerLog, SchedulerRuns

admin.site.register(SchedulerLog)


@admin.register(SchedulerRuns)
class SchedulerRunsAdmin(admin.ModelAdmin):
    list_display = ["start_time", "end_time", "run_duration", "status"]
    list_filter = ["status"]
    search_fields = ["details"]


@admin.register(ResourceIntervals)
class ResourceIntervalsAdmin(admin.ModelAdmin):
    list_display = ["resource", "task", "interval_start", "interval_end"]
    list_filter = ["resource", "task"]
    search_fields = ["resource", "task"]


@admin.register(ResourceAllocations)
class ResourceAllocationsAdmin(admin.ModelAdmin):
    list_display = ["resource", "task"]
    list_filter = ["resource", "task"]
    search_fields = ["resource", "task"]
