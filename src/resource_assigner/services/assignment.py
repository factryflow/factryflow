from api.permission_checker import AbstractPermissionService
from common.services import model_update

# validation error
from django.core.exceptions import PermissionDenied
from django.db import transaction
from job_manager.models import Task
from resource_manager.models import Resource

from resource_assigner.models import TaskResourceAssigment, TaskRuleAssignment, AssigmentRule


# ------------------------------------------------------------------------------
# Task Resource Assignment Services
# ------------------------------------------------------------------------------


class TaskResourceAssigmentService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        task: Task,
        resources: list[Resource] = [],
        custom_fields: dict = None,
    ) -> TaskResourceAssigment:
        # check permissions for create task resource assignment
        if not self.permission_service.check_for_permission(
            "add_taskresourceassigment"
        ):
            raise PermissionDenied()

        instance = TaskResourceAssigment.objects.create(
            task=task,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        instance.resources.set(resources)

        return instance

    @transaction.atomic
    def update(
        self, instance: TaskResourceAssigment, data: dict
    ) -> TaskResourceAssigment:
        # check permissions for update task resource assignment
        if not self.permission_service.check_for_permission(
            "change_taskresourceassigment"
        ):
            raise PermissionDenied()

        fields = [
            "task",
            "resource",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
        return instance

    @transaction.atomic
    def delete(self, instance: TaskResourceAssigment) -> None:
        # check permissions for delete task resource assignment
        if not self.permission_service.check_for_permission(
            "delete_taskresourceassigment"
        ):
            raise PermissionDenied()

        instance.delete()
        return True


# ------------------------------------------------------------------------------
# Task Rule Assignment Services
# ------------------------------------------------------------------------------


class TaskRuleAssignmentService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        task: Task,
        assigment_rule: AssigmentRule,
        is_applied: bool = False,
        custom_fields: dict = None,
    ) -> TaskRuleAssignment:
        # check permissions for create task rule assignment
        if not self.permission_service.check_for_permission("add_taskruleassignment"):
            raise PermissionDenied()

        instance = TaskRuleAssignment.objects.create(
            task=task,
            assigment_rule=assigment_rule,
            is_applied=is_applied,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        return instance

    @transaction.atomic
    def update(self, instance: TaskRuleAssignment, data: dict) -> TaskRuleAssignment:
        # check permissions for update task rule assignment
        if not self.permission_service.check_for_permission(
            "change_taskruleassignment"
        ):
            raise PermissionDenied()

        fields = [
            "task",
            "assigment_rule",
            "is_applied",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
        return instance

    @transaction.atomic
    def delete(self, instance: TaskRuleAssignment) -> None:
        # check permissions for delete task rule assignment
        if not self.permission_service.check_for_permission(
            "delete_taskruleassignment"
        ):
            raise PermissionDenied()

        instance.delete()
        return True
