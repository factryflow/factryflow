from api.permission_checker import AbstractPermissionService
from common.services import model_update
from common.utils import get_object

# validation error
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from microbatching.models.microbatch_rule import (
    MicrobatchRule,
    MicrobatchRuleCriteria,
)


class MicrobatchRuleCriteriaService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        microbatch_rule: MicrobatchRule,
        field: str,
        operator: str,
        value: str,
        custom_fields: dict = None,
    ) -> MicrobatchRuleCriteria:
        # check permissions for create microbatch rule criteria
        if not self.permission_service.check_for_permission(
            "add_microbatchrulecriteria"
        ):
            raise PermissionDenied()

        instance = MicrobatchRuleCriteria.objects.create(
            microbatch_rule=microbatch_rule,
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
        self, instance: MicrobatchRuleCriteria, data: dict
    ) -> MicrobatchRuleCriteria:
        # check permissions for update microbatch rule criteria
        if not self.permission_service.check_for_permission(
            "change_microbatchrulecriteria"
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
    def delete(self, instance: MicrobatchRuleCriteria) -> None:
        # check permissions for delete microbatch rule criteria
        if not self.permission_service.check_for_permission(
            "delete_microbatchrulecriteria"
        ):
            raise PermissionDenied()

        instance.delete()
        return True

    def validate_criteria_keys_throw_validation_error(
        self, criteria: list[dict]
    ) -> bool:
        keys = ["field", "operator", "value"]
        # check if keys exist
        for criteria_dict in criteria:
            if not all(key in criteria_dict for key in keys):
                missing_keys = [key for key in keys if key not in criteria_dict]
                raise ValidationError(
                    f"Microbatch Rule Criteria missing following keys: {', '.join(missing_keys)}"
                )

    def create_or_update_criteria(self, criteria: list[dict], instance: MicrobatchRule):
        # Create or update criteria
        for criteria_dict in criteria:
            criteria_id = criteria_dict.get("id")
            criteria_instance = get_object(
                model_or_queryset=MicrobatchRuleCriteria, id=criteria_id
            )
            if criteria_instance:
                self.update(
                    instance=criteria_instance,
                    data=criteria_dict,
                )
            else:
                # remove id if it does not exist
                criteria_dict.pop("id", None)

                # validate criteria keys
                self.validate_criteria_keys_throw_validation_error(
                    criteria=[criteria_dict]
                )
                self.create(
                    assigment_rule=instance,
                    **criteria_dict,
                )


class MicrobatchRuleService:
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

        self.microbatch_rule_criteria_service = MicrobatchRuleCriteriaService(user=user)

    @transaction.atomic
    def create(
        self,
        name: str,
        batch_size: int,
        criteria: list[dict] = [],
        custom_fields: dict = None,
    ) -> MicrobatchRule:
        # check permissions for create microbatch rule
        if not self.permission_service.check_for_permission("add_microbatchrule"):
            raise PermissionDenied()

        self.microbatch_rule_criteria_service.validate_criteria_keys_throw_validation_error(
            criteria=criteria
        )

        instance = MicrobatchRule.objects.create(
            name=name,
            batch_size=batch_size,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        # Create criteria
        for criteria_dict in criteria:
            self.microbatch_rule_criteria_service.create(
                microbatch_rule=instance,
                **criteria_dict,
                custom_fields=custom_fields,
            )

        return instance

    @transaction.atomic
    def update(self, instance: MicrobatchRule, data: dict) -> MicrobatchRule:
        # check permissions for update microbatch rule
        if not self.permission_service.check_for_permission("change_microbatchrule"):
            raise PermissionDenied()

        fields = [
            "name",
            "batch_size",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        criteria = data.get("criteria", [])

        if criteria:
            self.microbatch_rule_criteria_service.create_or_update_criteria(
                criteria=criteria, instance=instance
            )

        return instance

    @transaction.atomic
    def delete(self, instance: MicrobatchRule) -> None:
        # check permissions for delete microbatch rule
        if not self.permission_service.check_for_permission("delete_microbatchrule"):
            raise PermissionDenied()

        instance.delete()
        return True
