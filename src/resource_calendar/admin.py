from django.contrib import admin

from resource_calendar.models import WeeklyShiftTemplate, WeeklyShiftTemplateDetail, OperationalExceptionType, OperationalException


@admin.register(WeeklyShiftTemplate)
class WeeklyShiftTemplate(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']


@admin.register(WeeklyShiftTemplateDetail)
class WeeklyShiftTemplateDetail(admin.ModelAdmin):
    list_display = ['day_of_week','weekly_shift_template', 'created_at', 'created_by']
    list_filter = ['day_of_week', 'weekly_shift_template', 'created_at', 'created_by']
    search_fields = ['weekly_shift_template']


@admin.register(OperationalExceptionType)
class OperationalExceptionType(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']


@admin.register(OperationalException)
class OperationalException(admin.ModelAdmin):
    list_display = ['external_id','operational_exception_type', 'created_at', 'created_by']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']
