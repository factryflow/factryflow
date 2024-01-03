from django.contrib import admin
from .models import CustomField 


@admin.register(CustomField)
class CustomField(admin.ModelAdmin):
    list_display = ['name', 'label', 'content_type', 'field_type', 'created_at', 'created_by']
    list_filter =  ['field_type', 'created_at', 'created_by']
    search_fields = ['name', 'label']