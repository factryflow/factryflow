from api.permission_checker import AbstractPermissionService
from common.services import model_update
from common.utils import get_object

# validation error
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from job_manager.models import Task, WorkCenter
from resource_manager.models import Resource, ResourceGroup

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    TaskResourceAssigment,
)

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
        assigment_rule: AssigmentRule,
        resource: Resource = None,
        custom_fields: dict = None,
    ) -> TaskResourceAssigment:
        # check permissions for create task resource assignment
        if not self.permission_service.check_for_permission(
            "add_taskresourceassigment"
        ):
            raise PermissionDenied()

        instance = TaskResourceAssigment.objects.create(
            task=task,
            assigment_rule=assigment_rule,
            resource=resource,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

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
            "assigment_rule",
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


# ------------------------------------------------------------------------------
# Assigment Rule Services
# ------------------------------------------------------------------------------


class AssigmentRuleCriteriaService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        assigment_rule: AssigmentRule,
        field: str,
        operator: str,
        value: str,
        custom_fields: dict = None,
    ) -> AssigmentRuleCriteria:
        # check permissions for create assigment rule criteria
        if not self.permission_service.check_for_permission(
            "add_assigmentrulecriteria"
        ):
            raise PermissionDenied()

        instance = AssigmentRuleCriteria.objects.create(
            assigment_rule=assigment_rule,
            field=field,
            operator=operator,
            value=value,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        return instance

    @transaction.atomic
    def update(
        self, instance: AssigmentRuleCriteria, data: dict
    ) -> AssigmentRuleCriteria:
        # check permissions for update assigment rule criteria
        if not self.permission_service.check_for_permission(
            "change_assigmentrulecriteria"
        ):
            raise PermissionDenied()

        fields = [
            "field",
            "operator",
            "value",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
        return instance

    @transaction.atomic
    def delete(self, instance: AssigmentRuleCriteria) -> None:
        # check permissions for delete assigment rule criteria
        if not self.permission_service.check_for_permission(
            "delete_assigmentrulecriteria"
        ):
            raise PermissionDenied()

        instance.delete()
        return True


# ------------------------------------------------------------------------------
# Assigment Rule Services
# ------------------------------------------------------------------------------


class AssigmentRuleService:
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

        self.assignment_constraint_service = AssignmentConstraintService(user=user)
        self.assigment_rule_criteria_service = AssigmentRuleCriteriaService(user=user)

    def _validate_criteria_keys_throw_validation_error(
        self, criteria: list[dict]
    ) -> bool:
        keys = ["field", "operator", "value"]
        # check if keys exist
        for criteria_dict in criteria:
            if not all(key in criteria_dict for key in keys):
                missing_keys = [key for key in keys if key not in criteria_dict]
                raise ValidationError(
                    f"Assignment Rule Criteria missing following keys: {', '.join(missing_keys)}"
                )

    def _create_or_update_criteria(self, criteria: list[dict], instance: AssigmentRule):
        # Create or update criteria
        for criteria_dict in criteria:
            criteria_id = criteria_dict.get("id")
            criteria_instance = get_object(
                model_or_queryset=AssigmentRuleCriteria, id=criteria_id
            )
            if criteria_instance:
                self.assigment_rule_criteria_service.update(
                    instance=criteria_instance,
                    data=criteria_dict,
                )
            else:
                # validate criteria keys
                self._validate_criteria_keys_throw_validation_error(
                    criteria=[criteria_dict]
                )
                self.assigment_rule_criteria_service.create(
                    assigment_rule=instance,
                    **criteria_dict,
                )

    def _create_or_update_constraints(
        self, assignment_constraints: list[dict], instance: AssigmentRule
    ):
        # Create or update assignment constraints
        for assignment_constraint_dict in assignment_constraints:
            assignment_constraint_id = assignment_constraint_dict.get("id")
            assignment_constraint_instance = get_object(
                model_or_queryset=AssignmentConstraint, id=assignment_constraint_id
            )
            if assignment_constraint_instance:
                self.assignment_constraint_service.update(
                    instance=assignment_constraint_instance,
                    data=assignment_constraint_dict,
                )
            else:
                self.assignment_constraint_service.create(
                    assignment_rule=instance,
                    **assignment_constraint_dict,
                )

    @transaction.atomic
    def create(
        self,
        external_id: str,
        notes: str,
        name: str,
        description: str,
        is_active: bool,
        work_center: WorkCenter,
        assignment_constraints: list[dict] = [],
        criteria: list[dict] = [],
        custom_fields: dict = None,
    ) -> AssigmentRule:
        # check permissions for create assigment rule
        if not self.permission_service.check_for_permission("add_assigmentrule"):
            raise PermissionDenied()

        self._validate_criteria_keys_throw_validation_error(criteria=criteria)

        instance = AssigmentRule.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
            is_active=is_active,
            description=description,
            work_center=work_center,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        # Create assignment constraints
        for assignment_constraint_dict in assignment_constraints:
            self.assignment_constraint_service.create(
                assignment_rule=instance,
                **assignment_constraint_dict,
                custom_fields=custom_fields,
            )

        # Create criteria
        for criteria_dict in criteria:
            self.assigment_rule_criteria_service.create(
                assigment_rule=instance,
                **criteria_dict,
                custom_fields=custom_fields,
            )

        return instance

    @transaction.atomic
    def update(self, instance: AssigmentRule, data: dict) -> AssigmentRule:
        # check permissions for update assigment rule
        if not self.permission_service.check_for_permission("change_assigmentrule"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "is_active",
            "description",
            "resource_group",
            "work_center",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        criteria = data.get("criteria", [])

        self._create_or_update_criteria(criteria=criteria, instance=instance)

        assignment_constraints = data.get("assignment_constraints", [])

        self._create_or_update_constraints(
            assignment_constraints=assignment_constraints, instance=instance
        )

        return instance

    @transaction.atomic
    def delete(self, instance: AssigmentRule) -> None:
        # check permissions for delete assigment rule
        if not self.permission_service.check_for_permission("delete_assigmentrule"):
            raise PermissionDenied()

        instance.delete()
        return True
