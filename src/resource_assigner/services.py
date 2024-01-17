from common.services import model_update
from common.utils import get_object

# validation error
from django.core.exceptions import ValidationError
from django.db import transaction
from job_manager.models import Task, WorkCenter
from resource_manager.models import Resource, ResourcePool, WorkUnit

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    TaskResourceAssigment,
)


class TaskResourceAssigmentService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(self, *, task: Task, resource: Resource) -> TaskResourceAssigment:
        instance = TaskResourceAssigment.objects.create(
            task=task,
            resource=resource,
        )

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update(
        self, *, instance: TaskResourceAssigment, data: dict
    ) -> TaskResourceAssigment:
        fields = [
            "task",
            "resource",
        ]
        instance, _ = model_update(instance=instance, fields=fields, data=data)
        return instance

    @transaction.atomic
    def delete(self, *, instance: TaskResourceAssigment) -> None:
        instance.delete()


class AssignmentConstraintService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(
        self,
        *,
        task: Task = None,
        assignment_rule: AssigmentRule = None,
        resoruce_pool: ResourcePool = None,
        resources: list[Resource] = None,
        work_units: list[WorkUnit] = None,
        required_units: int = 1,
        is_direct: bool = True,
    ) -> AssignmentConstraint:
        instance = AssignmentConstraint.objects.create(
            task=task,
            assignment_rule=assignment_rule,
            resource_pool=resoruce_pool,
            required_units=required_units,
            is_direct=is_direct,
        )

        if resources:
            instance.resources.set(resources)

        if work_units:
            instance.work_units.set(work_units)

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update(
        self, *, instance: AssignmentConstraint, data: dict
    ) -> AssignmentConstraint:
        fields = [
            "resource_pool",
            "resources",
            "work_units",
            "required_units",
        ]
        instance, _ = model_update(instance=instance, fields=fields, data=data)
        return instance

    @transaction.atomic
    def delete(self, *, instance: AssignmentConstraint) -> None:
        instance.delete()


# ------------------------------------------------------------------------------
# Assigment Rule Services
# ------------------------------------------------------------------------------


class AssigmentRuleCriteriaService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(
        self,
        *,
        assigment_rule: AssigmentRule,
        field: str,
        operator: str,
        value: str,
    ) -> AssigmentRuleCriteria:
        instance = AssigmentRuleCriteria.objects.create(
            assigment_rule=assigment_rule,
            field=field,
            operator=operator,
            value=value,
        )

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update(
        self, *, instance: AssigmentRuleCriteria, data: dict
    ) -> AssigmentRuleCriteria:
        fields = [
            "field",
            "operator",
            "value",
        ]
        instance, _ = model_update(instance=instance, fields=fields, data=data)
        return instance

    @transaction.atomic
    def delete(self, *, instance: AssigmentRuleCriteria) -> None:
        instance.delete()


class AssigmentRuleService:
    def __init__(self, user):
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
                    is_direct=False,
                )

    @transaction.atomic
    def create(
        self,
        *,
        name: str,
        description: str,
        work_center: WorkCenter,
        assignment_constraints: list[dict] = [],
        criteria: list[dict] = [],
    ) -> AssigmentRule:
        self._validate_criteria_keys_throw_validation_error(criteria=criteria)

        instance = AssigmentRule.objects.create(
            name=name,
            description=description,
            work_center=work_center,
        )

        instance.full_clean()
        instance.save()

        # Create assignment constraints
        for assignment_constraint_dict in assignment_constraints:
            self.assignment_constraint_service.create(
                assignment_rule=instance,
                **assignment_constraint_dict,
                is_direct=False,
            )

        # Create criteria
        for criteria_dict in criteria:
            self.assigment_rule_criteria_service.create(
                assigment_rule=instance,
                **criteria_dict,
            )

        return instance

    @transaction.atomic
    def update(self, *, instance: AssigmentRule, data: dict) -> AssigmentRule:
        fields = [
            "name",
            "description",
            "resource_group",
            "work_center",
        ]
        instance, _ = model_update(instance=instance, fields=fields, data=data)

        criteria = data.get("criteria", [])

        self._create_or_update_criteria(criteria=criteria, instance=instance)

        assignment_constraints = data.get("assignment_constraints", [])

        self._create_or_update_constraints(
            assignment_constraints=assignment_constraints, instance=instance
        )

        return instance

    @transaction.atomic
    def delete(self, *, instance: AssigmentRule) -> None:
        instance.delete()
