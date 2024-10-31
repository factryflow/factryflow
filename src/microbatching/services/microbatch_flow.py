from api.permission_checker import AbstractPermissionService
from common.services import model_update

# validation error
from django.core.exceptions import PermissionDenied
from django.db import transaction

from microbatching.models.microbatch_flow import MicrobatchFlow
from microbatching.models.microbatch_rule import MicrobatchRule


class MicrobatchFlowService:
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        name: str,
        description: str,
        start_rule: MicrobatchRule,
        end_rule: MicrobatchRule,
        min_flow_length: int,
        max_flow_length: int,
        batch_size: int,
        custom_fields: dict = None,
    ) -> MicrobatchFlow:
        # check permissions for create microbatch flow
        if not self.permission_service.check_for_permission("add_microbatchflow"):
            raise PermissionDenied()

        instance = MicrobatchFlow.objects.create(
            name=name,
            description=description,
            start_rule=start_rule,
            end_rule=end_rule,
            min_flow_length=min_flow_length,
            max_flow_length=max_flow_length,
            batch_size=batch_size,
            custom_fields=custom_fields,
        )

        instance.full_clean()
        instance.save(user=self.user)

        return instance

    @transaction.atomic
    def update(self, instance: MicrobatchFlow, data: dict) -> MicrobatchFlow:
        # check permissions for update microbatch rule
        if not self.permission_service.check_for_permission("change_microbatchflow"):
            raise PermissionDenied()

        fields = [
            "name",
            "description",
            "start_rule",
            "end_rule",
            "min_flow_length",
            "max_flow_length",
            "batch_size",
            "custom_fields",
        ]
        instance, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return instance

    @transaction.atomic
    def delete(self, instance: MicrobatchFlow) -> None:
        # check permissions for delete microbatch rule
        if not self.permission_service.check_for_permission("delete_microbatchflow"):
            raise PermissionDenied()

        instance.delete()
        return True
