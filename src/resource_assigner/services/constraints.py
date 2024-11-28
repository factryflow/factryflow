from api.permission_checker import AbstractPermissionService
from common.services import model_update

# validation error
from django.core.exceptions import PermissionDenied
from django.db import transaction
from job_manager.models import Task
from resource_manager.models import Resource, ResourceGroup

from resource_assigner.models import (
    AssigmentRule,
    AssignmentConstraint,
)


# ------------------------------------------------------------------------------
# Assignment Constraint Services
# ------------------------------------------------------------------------------


class AssignmentConstraintService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        task: Task = None,
        assignment_rule: AssigmentRule = None,
        resource_group: ResourceGroup = None,
        resources: list[Resource] = None,
        use_all_resources: bool = True,
        resource_count: int = 1,
        custom_fields: dict = None,
    ) -> AssignmentConstraint:
        # check permissions for create assignment constraint
        if not self.permission_service.check_for_permission("add_assignmentconstraint"):
            raise PermissionDenied()

        instance = AssignmentConstraint.objects.create(
            task=task,
            assignment_rule=assignment_rule,
            resource_group=resource_group,
            use_all_resources=use_all_resources,
            resource_count=resource_count,
            custom_fields=custom_fields,
        )

        if resources:
            instance.resources.set(resources)

        instance.full_clean()
        instance.save(user=self.user)

        return instance

    @transaction.atomic
    def update(
        self, instance: AssignmentConstraint, data: dict
    ) -> AssignmentConstraint:
        # check permissions for update assignment constraint
        if not self.permission_service.check_for_permission(
            "change_assignmentconstraint"
        ):
            raise PermissionDenied()

        fields = [
            "resource_group",
            "resources",
            "task",
            "assignment_rule",
            "use_all_resources",
            "resource_count",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
        return instance

    @transaction.atomic
    def delete(self, instance: AssignmentConstraint) -> None:
        # check permissions for delete assignment constraint
        if not self.permission_service.check_for_permission(
            "delete_assignmentconstraint"
        ):
            raise PermissionDenied()

        instance.delete()
        return True
