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
    TaskResourceAssigment,
)


class TaskResourceAssigmentService(AbstractPermissionService):
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
        # check permissions for add task resource assigment
        if not self.check_for_permission("add_taskresourceassigment"):
            raise PermissionDenied()

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
        # check permissions for update task resource assigment
        if not self.check_for_permission("change_taskresourceassigment"):
            raise PermissionDenied()

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
        # check permissions for delete task resource assigment
        if not self.check_for_permission("delete_taskresourceassigment"):
            raise PermissionDenied()

        instance.delete()


# ------------------------------------------------------------------------------
# Assigment Rule Services
# ------------------------------------------------------------------------------


class AssigmentRuleCriteriaService(AbstractPermissionService):
    @transaction.atomic
    def create(
        self,
        *,
        assigment_rule: AssigmentRule,
        field: str,
        operator: str,
        value: str,
    ) -> AssigmentRuleCriteria:
        # check permissions for create assigment rule criteria
        if not self.check_for_permission("add_assigmentrulecriteria"):
            raise PermissionDenied()

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
        # check permissions for update assigment rule criteria
        if not self.check_for_permission("change_assigmentrulecriteria"):
            raise PermissionDenied()

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
        # check permissions for delete assigment rule criteria
        if not self.check_for_permission("delete_assigmentrulecriteria"):
            raise PermissionDenied()

        instance.delete()


class AssigmentRuleService(AbstractPermissionService):
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
        # check permissions for create assigment rule
        if not self.check_for_permission("add_assigmentrule"):
            raise PermissionDenied()

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
            AssigmentRuleCriteriaService(user=self.user).create(
                assigment_rule=instance,
                field=criteria_dict["field"],
                operator=criteria_dict["operator"],
                value=criteria_dict["value"],
            )

        return instance

    @transaction.atomic
    def update(self, *, instance: AssigmentRule, data: dict) -> AssigmentRule:
        # check permissions for update assigment rule
        if not self.check_for_permission("change_assigmentrule"):
            raise PermissionDenied()

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
                AssigmentRuleCriteriaService(user=self.user).update(
                    instance=criteria_instance,
                    data=criteria_dict,
                )
            else:
                # validate criteria keys
                self._validate_criteria_keys_throw_validation_eror(
                    criteria=[criteria_dict]
                )
                AssigmentRuleCriteriaService(user=self.user).create(
                    assigment_rule=instance,
                    field=criteria_dict.get("field"),
                    operator=criteria_dict.get("operator"),
                    value=criteria_dict.get("value"),
                )

        return instance

    @transaction.atomic
    def delete(self, *, instance: AssigmentRule) -> None:
        # check permissions for delete assigment rule
        if not self.check_for_permission("delete_assigmentrule"):
            raise PermissionDenied()

        instance.delete()
