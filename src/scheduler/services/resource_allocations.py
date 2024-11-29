from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from job_manager.models import Task
from resource_manager.models import Resource

from scheduler.models import ResourceAllocations, SchedulerRuns


# --------------------------------------------------------
# Resource Allocations Service
# --------------------------------------------------------


class ResourceAllocationsService(AbstractPermissionService):
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def get_all_resource_allocations(self):
        # get all resource allocations
        if not self.permission_service.check_for_permission("view_resourceallocations"):
            raise PermissionDenied(
                "You do not have permission to view resource allocations"
            )

        return ResourceAllocations.objects.all()

    def get_resource_allocations_by_id(self, resource_id=None, task_id=None):
        # Check permission
        if not self.permission_service.check_for_permission("view_resourceallocations"):
            raise PermissionDenied(
                "You do not have permission to view resource allocations"
            )

        filters = Q()
        if resource_id:
            filters &= Q(resource_id=resource_id)
        if task_id:
            filters &= Q(task_id=task_id)

        # Apply filters to the queryset
        queryset = ResourceAllocations.objects.filter(filters)

        return queryset

    @transaction.atomic
    def create(
        self,
        scheduler_run: SchedulerRuns,
        resource: Resource,
        task: Task,
    ):
        # check permissions
        if not self.permission_service.check_for_permission("add_resourceallocations"):
            raise PermissionDenied(
                "You do not have permission to add resource allocations"
            )

        resource_allocation = ResourceAllocations.objects.create(
            run_id=scheduler_run,
            resource=resource,
            task=task,
        )

        resource_allocation.full_clean()
        resource_allocation.save()
        return resource_allocation

    @transaction.atomic
    def update(self, instance: ResourceAllocations, data: dict):
        if not self.permission_service.check_for_permission(
            "change_resourceallocations"
        ):
            raise PermissionDenied(
                "You do not have permission to change resource allocations"
            )

        fields = ["run_id", "resource", "task"]
        resource_allocation = model_update(
            instance=instance, data=data, fields=fields, user=self.user
        )

        return resource_allocation

    @transaction.atomic
    def delete(self, instance: ResourceAllocations):
        if not self.permission_service.check_for_permission(
            "delete_resourceallocations"
        ):
            raise PermissionDenied(
                "You do not have permission to delete resource allocations"
            )

        instance.delete()
        return True
