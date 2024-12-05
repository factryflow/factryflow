from api.permission_checker import AbstractPermissionService
from django.contrib.contenttypes.models import ContentType
from common.services import model_update
from common.utils import get_object
from common.utils.criteria import get_all_nested_group_ids
from common.models import NestedCriteria, NestedCriteriaGroup

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

    def _create_or_update_nested_criteria(
        self, microbatch_rule, group_data, parent_group=None
    ):
        """
        Creates a nested group criteria structure for a given microbatch rule.

        This method creates a NestedCriteriaGroup instance and associates it with the provided
        microbatch rule and group data. It also handles the creation of nested criteria and inner
        groups recursively.

        Args:
            microbatch_rule: The microbatch rule to associate with the nested group criteria.
            group_data (dict): A dictionary containing the group data, including operator, criteria,
            and inner groups.
            parent_group (NestedCriteriaGroup, optional): The parent group to nest the created group
            under. Defaults to None.

        Returns:
            NestedCriteriaGroup: The created nested group criteria instance.
        """

        if group_data["id"]:
            group_instance = get_object(
                model_or_queryset=NestedCriteriaGroup, id=group_data["id"]
            )
            group_instance.operator = group_data["operator"]
            group_instance.save()
        else:
            group_instance = NestedCriteriaGroup.objects.create(
                content_type=ContentType.objects.get_for_model(MicrobatchRule),
                object_id=microbatch_rule.id,
                operator=group_data["operator"],
                parent_group=parent_group,
            )
            group_instance.full_clean()
            group_instance.save()

        for criteria in group_data.get("criteria", []):
            # remove unwanted fields
            criteria.pop("type", None)
            criteria_id = criteria.pop("id", None)

            if criteria_id:
                criteria_instance = self.microbatch_rule_criteria_service.update(
                    instance=get_object(
                        model_or_queryset=MicrobatchRuleCriteria, id=criteria_id
                    ),
                    data=criteria,
                )
            else:
                criteria_instance = self.microbatch_rule_criteria_service.create(
                    microbatch_rule=microbatch_rule,
                    **criteria,
                )

            NestedCriteria.objects.update_or_create(
                group=group_instance,
                content_type=ContentType.objects.get_for_model(MicrobatchRuleCriteria),
                object_id=criteria_instance.id,
            )

        for inner_group in group_data.get("innerGroups", []):
            self._create_or_update_nested_criteria(
                microbatch_rule, inner_group, parent_group=group_instance
            )

        return group_instance

    def _delete_nested_criteria_group(self, data):
        """
        Deletes nested criteria groups and criteria based on the provided data.

        Args:
            data (dict): A dictionary containing the following keys:
            - "groupIds" (list): A list of group IDs to be deleted.
            - "criteriaIds" (list): A list of criteria IDs to be deleted.

        Returns:
            bool: True if the deletion process completes successfully.
        """
        group_ids = data.get("groupIds", [])
        criteria_ids = data.get("criteriaIds", [])

        group_ids_to_delete = []

        if group_ids:
            parent_groups = NestedCriteriaGroup.objects.filter(id__in=group_ids)
            for group in parent_groups:
                group_ids_to_delete.extend(get_all_nested_group_ids(group=group))

            groups_to_delete = NestedCriteriaGroup.objects.filter(
                id__in=group_ids_to_delete
            )

            nested_criteria_to_delete = NestedCriteria.objects.filter(
                group__in=groups_to_delete
            )
            rule_criteria_ids = nested_criteria_to_delete.values_list(
                "object_id", flat=True
            )

            MicrobatchRuleCriteria.objects.filter(id__in=rule_criteria_ids).delete()
            nested_criteria_to_delete.delete()
            groups_to_delete.delete()

        if criteria_ids:
            NestedCriteria.objects.filter(
                content_type=ContentType.objects.get_for_model(MicrobatchRuleCriteria),
                object_id__in=criteria_ids,
            ).delete()
            MicrobatchRuleCriteria.objects.filter(id__in=criteria_ids).delete()

        return True

    @transaction.atomic
    def create(
        self,
        name: str,
        criteria: list[dict] = [],
        custom_fields: dict = None,
        nested_criteria: list[dict] = [],
    ) -> MicrobatchRule:
        # check permissions for create microbatch rule
        if not self.permission_service.check_for_permission("add_microbatchrule"):
            raise PermissionDenied()

        self.microbatch_rule_criteria_service.validate_criteria_keys_throw_validation_error(
            criteria=criteria
        )

        instance = MicrobatchRule.objects.create(
            name=name,
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

        # create nested group criteria if any
        if len(nested_criteria) > 0:
            for group in nested_criteria:
                self._create_or_update_nested_criteria(
                    microbatch_rule=instance,
                    group_data=group,
                )

        return instance

    @transaction.atomic
    def update(self, instance: MicrobatchRule, data: dict) -> MicrobatchRule:
        # check permissions for update microbatch rule
        if not self.permission_service.check_for_permission("change_microbatchrule"):
            raise PermissionDenied()

        fields = [
            "name",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        # Update criteria
        criteria = data.get("criteria", [])

        if criteria:
            self.microbatch_rule_criteria_service.create_or_update_criteria(
                criteria=criteria, instance=instance
            )

        # update nested group criteria if any
        nested_criteria = data.get("nested_criteria", [])
        if nested_criteria:
            for group in nested_criteria:
                self._create_or_update_nested_criteria(
                    microbatch_rule=instance,
                    group_data=group,
                )

        # delete nested group criteria if any
        delete_nested_criteria_group = data.get("delete_nested_criteria_group", {})
        self._delete_nested_criteria_group(data=delete_nested_criteria_group)

        return instance

    @transaction.atomic
    def delete(self, instance: MicrobatchRule) -> None:
        # check permissions for delete microbatch rule
        if not self.permission_service.check_for_permission("delete_microbatchrule"):
            raise PermissionDenied()

        instance.delete()
        return True
