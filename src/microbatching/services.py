from api.permission_checker import AbstractPermissionService
from common.services import model_update

# validation error
from django.core.exceptions import PermissionDenied
from django.db import transaction
from job_manager.models import WorkCenter

from microbatching.models import MicrobatchRule


class MicrobatchRuleService:
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        item_name: str,
        work_center: WorkCenter,
        batch_size: int,
        custom_fields: dict = None,
    ) -> MicrobatchRule:
        # check permissions for create assigment rule
        if not self.permission_service.check_for_permission("add_microbatchrule"):
            raise PermissionDenied()

        instance = MicrobatchRule.objects.create(
            item_name=item_name,
            batch_size=batch_size,
            work_center=work_center,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        return instance

    @transaction.atomic
    def update(self, instance: MicrobatchRule, data: dict) -> MicrobatchRule:
        # check permissions for update assigment rule
        if not self.permission_service.check_for_permission("change_microbatchrule"):
            raise PermissionDenied()

        fields = [
            "external_id",
            "item_name",
            "batch_size",
            "work_center",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return instance

    @transaction.atomic
    def delete(self, instance: MicrobatchRule) -> None:
        # check permissions for delete assigment rule
        if not self.permission_service.check_for_permission("delete_microbatchrule"):
            raise PermissionDenied()

        instance.delete()
        return True
