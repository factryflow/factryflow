from common.services import model_update
from common.utils import get_object

# validation error
from django.core.exceptions import ValidationError
from django.db import transaction
from job_manager.models import Task, WorkCenter
from resource_manager.models import Resource, ResourceGroup

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    TaskResourceAssigment,
)


class TaskResourceAssigmentService:
    def __init__(self, user=None):
        self.user = user

    @transaction.atomic
    def create(
        self,
        *,
        task: Task,
        resource_group: ResourceGroup,
        resources: list[Resource] = None,
        resource_count: int = None,
        use_all_resources: bool = False,
        is_direct: bool = True,
    ) -> TaskResourceAssigment:
        instance = TaskResourceAssigment.objects.create(
            task=task,
            resource_group=resource_group,
            resource_count=resource_count,
            use_all_resources=use_all_resources,
            is_direct=is_direct,
        )

        if resources:
            instance.resources.set(resources)

        instance.full_clean()
        instance.save(user=self.user)

        return instance

    @transaction.atomic
    def update(
        self, *, instance: TaskResourceAssigment, data: dict
    ) -> TaskResourceAssigment:
        fields = [
            "task",
            "resource_group",
            "resources",
            "resource_count",
            "use_all_resources",
            "is_direct",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
        return instance

    @transaction.atomic
    def delete(self, *, instance: TaskResourceAssigment) -> None:
        instance.delete()


# ------------------------------------------------------------------------------
# Assigment Rule Services
# ------------------------------------------------------------------------------


class AssigmentRuleCriteriaService:
    def __init__(self, user=None):
        self.user = user

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
        instance.save(user=self.user)

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
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )
        return instance

    @transaction.atomic
    def delete(self, *, instance: AssigmentRuleCriteria) -> None:
        instance.delete()


class AssigmentRuleService:
    def __init__(self, user=None):
        self.user = user

    def _validate_criteria_keys_throw_validation_eror(
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

    @transaction.atomic
    def create(
        self,
        *,
        name: str,
        description: str,
        resource_group: ResourceGroup,
        work_center: WorkCenter,
        criteria: list[dict] = [],
    ) -> AssigmentRule:
        self._validate_criteria_keys_throw_validation_eror(criteria=criteria)

        instance = AssigmentRule.objects.create(
            name=name,
            description=description,
            resource_group=resource_group,
            work_center=work_center,
        )

        instance.full_clean()
        instance.save(user=self.user)

        # Create criteria
        for criteria_dict in criteria:
            AssigmentRuleCriteriaService().create(
                assigment_rule=instance,
                field=criteria_dict["field"],
                operator=criteria_dict["operator"],
                value=criteria_dict["value"],
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
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        criteria = data.get("criteria", [])

        # Create or update criteria
        for criteria_dict in criteria:
            criteria_id = criteria_dict.get("id")
            criteria_instance = get_object(
                model_or_queryset=AssigmentRuleCriteria, id=criteria_id
            )
            if criteria_instance:
                AssigmentRuleCriteriaService().update(
                    instance=criteria_instance,
                    data=criteria_dict,
                )
            else:
                # validate criteria keys
                self._validate_criteria_keys_throw_validation_eror(
                    criteria=[criteria_dict]
                )
                AssigmentRuleCriteriaService().create(
                    assigment_rule=instance,
                    field=criteria_dict.get("field"),
                    operator=criteria_dict.get("operator"),
                    value=criteria_dict.get("value"),
                )

        return instance

    @transaction.atomic
    def delete(self, *, instance: AssigmentRule) -> None:
        instance.delete()
