from collections import defaultdict
from datetime import datetime, time

from django.db.models import Q

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from resource_manager.models import Resource

from .models import (
    SchedulerRuns,
    ResourceIntervals,
    ResourceAllocations
)


class ResourceIntervalsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_all_resource_intervals(self):
        # get all resource intervals
        if not self.permission_service.check_for_permission("view_resourcentervals"):
            raise PermissionDenied("You do not have permission to view resource intervals")
        
        return self.resource_intervals.objects.all()
    

    def get_resource_intervals_by_id(self, interval_id=None, resource_id=None, task_id=None):
        # Check permission
        if not self.permission_service.check_for_permission("view_resourcentervals"):
            raise PermissionDenied("You do not have permission to view resource intervals")

        filters = Q()
        if interval_id:
            filters &= Q(id=interval_id)
        if resource_id:
            filters &= Q(resource_id=resource_id)
        if task_id:
            filters &= Q(task_id=task_id)

        # Apply filters to the queryset
        queryset = self.resource_intervals.objects.filter(filters)

        return queryset


    def create_resource_intervals(self, resource, task, interval_start, interval_end):
        # check permissions
        if not self.permission_service.check_for_permission("add_resourcentervals"):
            raise PermissionDenied("You do not have permission to add resource intervals")

        resource_interval = ResourceIntervals.objects.create(
            resource=resource,
            task=task,
            interval_start=interval_start,
            interval_end=interval_end
        )

        resource_interval.full_clean()
        resource_interval.save()
        return resource_interval


    def update_resource_intervals(self, id, resource, task, interval_start, interval_end):
        if self.permission_service.check_for_permission("change_resourcentervals"):
            raise PermissionDenied("You do not have permission to change resource intervals")

        resource_interval = self.resource_intervals.objects.get(id=id)
        resource_interval.resource = resource
        resource_interval.task = task
        resource_interval.interval_start = interval_start
        resource_interval.interval_end = interval_end

        resource_interval.full_clean()
        resource_interval.save()
        return resource_interval


    def delete_resource_intervals(self, id):
        if not self.permission_service.check_for_permission("delete_resourcentervals"):
            raise PermissionDenied("You do not have permission to delete resource intervals")
        
        resource_interval = self.resource_intervals.objects.get(id=id)
        resource_interval.delete()



class ResourceAllocationsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_all_resource_allocations(self):
        # get all resource allocations
        if not self.permission_service.check_for_permission("view_resourceallocations"):
            raise PermissionDenied("You do not have permission to view resource allocations")
        
        return self.resource_allocations.objects.all()
    

    def get_resource_allocations_by_id(self, allocation_id=None, resource_id=None, task_id=None):
        # Check permission
        if not self.permission_service.check_for_permission("view_resourceallocations"):
            raise PermissionDenied("You do not have permission to view resource allocations")

        filters = Q()
        if allocation_id:
            filters &= Q(id=allocation_id)
        if resource_id:
            filters &= Q(resource_id=resource_id)
        if task_id:
            filters &= Q(task_id=task_id)

        # Apply filters to the queryset
        queryset = self.resource_allocations.objects.filter(filters)

        return queryset


    def create_resource_allocations(self, resource, task, start_datetime=None, end_datetime=None):
        # check permissions
        if not self.permission_service.check_for_permission("add_resourceallocations"):
            raise PermissionDenied("You do not have permission to add resource allocations")

        resource_allocation = ResourceAllocations.objects.create(
            resource=resource,
            task=task,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )

        resource_allocation.full_clean()
        resource_allocation.save()
        return resource_allocation


    def update_resource_allocations(self, id, resource, task, start_datetime=None, end_datetime=None):
        if self.permission_service.check_for_permission("change_resourceallocations"):
            raise PermissionDenied("You do not have permission to change resource allocations")

        resource_allocation = self.resource_allocations.objects.get(id=id)
        resource_allocation.resource = resource
        resource_allocation.task = task
        resource_allocation.start_datetime = start_datetime
        resource_allocation.end_datetime = end_datetime

        resource_allocation.full_clean()
        resource_allocation.save()
        return resource_allocation


    def delete_resource_allocations(self, id):
        if not self.permission_service.check_for_permission("delete_resourceallocations"):
            raise PermissionDenied("You do not have permission to delete resource allocations")
        
        resource_allocation = self.resource_allocations.objects.get(id=id)
        resource_allocation.delete()



class SchedulerRunsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_all_scheduler_runs(self):
        # get all scheduler runs
        if not self.permission_service.check_for_permission("view_schedulerruns"):
            raise PermissionDenied("You do not have permission to view scheduler runs")
        
        return self.scheduler_runs.objects.all()
    

    def get_scheduler_runs_by_id(self, run_id=None):
        # Check permission
        if not self.permission_service.check_for_permission("view_schedulerruns"):
            raise PermissionDenied("You do not have permission to view scheduler runs")

        filters = Q()
        if run_id:
            filters &= Q(id=run_id)

        # Apply filters to the queryset
        queryset = self.scheduler_runs.objects.filter(filters)

        return queryset


    def create_scheduler_runs(self, start_time, end_time=None, run_duration=None, details=None, status=None):
        # check permissions
        if not self.permission_service.check_for_permission("add_schedulerruns"):
            raise PermissionDenied("You do not have permission to add scheduler runs")

        scheduler_run = SchedulerRuns.objects.create(
            start_time=start_time,
            end_time=end_time,
            run_duration=run_duration,
            details=details,
            status=status
        )

        scheduler_run.full_clean()
        scheduler_run.save()
        return scheduler_run


    def update_scheduler_runs(self, id, start_time, end_time=None, run_duration=None, details=None, status=None):
        if self.permission_service.check_for_permission("change_schedulerruns"):
            raise PermissionDenied("You do not have permission to change scheduler runs")

        scheduler_run = self.scheduler_runs.objects.get(id=id)
        scheduler_run.start_time = start_time
        scheduler_run.end_time = end_time
        scheduler_run.run_duration = run_duration
        scheduler_run.details = details
        scheduler_run.status = status

        scheduler_run.full_clean()
        scheduler_run.save()
        return scheduler_run


    def delete_scheduler_runs(self, id):
        if not self.permission_service.check_for_permission("delete_schedulerruns"):
            raise PermissionDenied("You do not have permission to delete scheduler runs")
        
        scheduler_run = self.scheduler_runs.objects.get(id=id)
        scheduler_run.delete()