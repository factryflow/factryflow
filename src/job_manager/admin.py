from django.contrib import admin
from .models.dependency import DependencyType, Dependency
from .models.job import JobType, Job
from .models.task import TaskType, Task, WorkCenter

@admin.register(DependencyType)
class DependencyType(admin.ModelAdmin):
    list_display = ['name','created_at', 'created_by']
    list_filter = ('created_at','created_by')
    search_fields = ['name']


@admin.register(Dependency)
class Dependency(admin.ModelAdmin):
    list_display = ['name','external_id','notes','created_at', 'created_by']
    list_filter = ['external_id','notes','created_at', 'created_by']
    search_fields = ['name','external_id']



@admin.register(WorkCenter)
class WorkCenter(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']



@admin.register(JobType)
class JobType(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']


@admin.register(Job)
class Job(admin.ModelAdmin):
    list_display = ['name', 'job_type', 'priority' ,'external_id','job_status','due_date', 'created_at', 'created_by']
    list_filter = ['job_type','job_status', 'created_at', 'created_by']
    search_fields = ['name',]


@admin.register(TaskType)
class TaskType(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ['name', 'id','external_id', 'task_type', 'created_at', 'created_by']
    list_filter = ['task_type', 'created_at', 'created_by']
    search_fields = ['name']