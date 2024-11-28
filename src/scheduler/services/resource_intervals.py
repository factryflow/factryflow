from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from job_manager.models import Task
from resource_manager.models import Resource

from scheduler.models import ResourceIntervals, SchedulerRuns

# --------------------------------------------------------
# Resource Intervals Service
# --------------------------------------------------------


class ResourceIntervalsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_all_resource_intervals(self):
        # get all resource intervals
        if not self.permission_service.check_for_permission("view_resourcentervals"):
            raise PermissionDenied(
                "You do not have permission to view resource intervals"
            )

        return ResourceIntervals.objects.all()

    def get_resource_intervals_by_id(
        self, interval_id=None, resource_id=None, task_id=None
    ):
        # Check permission
        if not self.permission_service.check_for_permission("view_resourcentervals"):
            raise PermissionDenied(
                "You do not have permission to view resource intervals"
            )

        filters = Q()
        if interval_id:
            filters &= Q(id=interval_id)
        if resource_id:
            filters &= Q(resource_id=resource_id)
        if task_id:
            filters &= Q(task_id=task_id)

        # Apply filters to the queryset
        queryset = ResourceIntervals.objects.filter(filters)

        return queryset

    @transaction.atomic
    def create(
        self,
        scheduler_run: SchedulerRuns,
        resource: Resource,
        task: Task,
        interval_start,
        interval_end,
    ):
        # check permissions
        if not self.permission_service.check_for_permission("add_resourceintervals"):
            raise PermissionDenied(
                "You do not have permission to add resource intervals"
            )

        resource_interval = ResourceIntervals.objects.create(
            run_id=scheduler_run,
            resource=resource,
            task=task,
            interval_start=interval_start,
            interval_end=interval_end,
        )

        resource_interval.full_clean()
        resource_interval.save()
        return resource_interval

    @transaction.atomic
    def update(self, instance: ResourceIntervals, data: dict):
        if not self.permission_service.check_for_permission("change_resourceintervals"):
            raise PermissionDenied(
                "You do not have permission to change resource intervals"
            )

        fields = ["run_id", "resource", "task", "interval_start", "interval_end"]
        resource_interval = model_update(
            instance=instance, data=data, fields=fields, user=self.user
        )

        return resource_interval

    @transaction.atomic
    def delete(self, instance: ResourceIntervals):
        if not self.permission_service.check_for_permission("delete_resourceintervals"):
            raise PermissionDenied(
                "You do not have permission to delete resource intervals"
            )

        instance.delete()
        return True
