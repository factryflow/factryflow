# from api.permission_checker import AbstractPermissionService
# from common.services import model_update
# from common.utils import get_object

# # validation error
# from django.core.exceptions import PermissionDenied, ValidationError
# from django.db import transaction
# from job_manager.models import WorkCenter

# from microbatching.models.microbatch_flow import MicrobatchFlow, MicrobatchFlowStep


# class MicrobatchFlowStepService:
#     def __init__(self, user) -> None:
#         self.user = user
#         self.permission_service = AbstractPermissionService(user=user)

#     @transaction.atomic
#     def create(
#         self,
#         microbatch_flow: MicrobatchFlow,
#         field: str,
#         operator: str,
#         value: str,
#         custom_fields: dict = None,
#     ) -> MicrobatchFlowStep:
#         # check permissions for create microbatch rule step
#         if not self.permission_service.check_for_permission("add_microbatchflowstep"):
#             raise PermissionDenied()

#         instance = MicrobatchFlowStep.objects.create(
#             microbatch_flow=microbatch_flow,
#             field=field,
#             operator=operator,
#             value=value,
#             custom_fields=custom_fields,
#         )

#         instance.full_clean()
#         instance.save(user=self.user)

#         return instance

#     @transaction.atomic
#     def update(self, instance: MicrobatchFlowStep, data: dict) -> MicrobatchFlowStep:
#         # check permissions for update microbatch rule step
#         if not self.permission_service.check_for_permission(
#             "change_microbatchflowstep"
#         ):
#             raise PermissionDenied()

#         fields = [
#             "field",
#             "operator",
#             "value",
#             "custom_fields",
#         ]
#         instance, _ = model_update(
#             instance=instance, fields=fields, data=data, user=self.user
#         )
#         return instance

#     @transaction.atomic
#     def delete(self, instance: MicrobatchFlowStep) -> None:
#         # check permissions for delete microbatch rule step
#         if not self.permission_service.check_for_permission(
#             "delete_microbatchflowstep"
#         ):
#             raise PermissionDenied()

#         instance.delete()
#         return True

#     def validate_step_keys_throw_validation_error(self, step: list[dict]) -> bool:
#         keys = ["field", "operator", "value"]
#         # check if keys exist
#         for step_dict in step:
#             if not all(key in step_dict for key in keys):
#                 missing_keys = [key for key in keys if key not in step_dict]
#                 raise ValidationError(
#                     f"Microbatch Rule Criteria missing following keys: {', '.join(missing_keys)}"
#                 )

#     def create_or_update_step(self, step: list[dict], instance: MicrobatchFlow):
#         # Create or update step
#         for step_dict in step:
#             step_id = step_dict.get("id")
#             step_instance = get_object(model_or_queryset=MicrobatchFlowStep, id=step_id)
#             if step_instance:
#                 self.update(
#                     instance=step_instance,
#                     data=step_dict,
#                 )
#             else:
#                 # remove id if it does not exist
#                 step_dict.pop("id", None)

#                 # validate step keys
#                 self.validate_step_keys_throw_validation_error(step=[step_dict])
#                 self.create(
#                     assigment_rule=instance,
#                     **step_dict,
#                 )


# class MicrobatchFlowService:
#     def __init__(self, user):
#         self.user = user
#         self.permission_service = AbstractPermissionService(user=user)

#         self.microbatch_flow_step_service = MicrobatchFlowStepService(user=user)

#     @transaction.atomic
#     def create(
#         self,
#         item_name: str,
#         work_center: WorkCenter,
#         batch_size: int,
#         step: list[dict] = [],
#         custom_fields: dict = None,
#     ) -> MicrobatchFlow:
#         # check permissions for create microbatch rule
#         if not self.permission_service.check_for_permission("add_microbatchrule"):
#             raise PermissionDenied()

#         self.microbatch_flow_step_service.validate_step_keys_throw_validation_error(
#             step=step
#         )

#         instance = MicrobatchFlow.objects.create(
#             item_name=item_name,
#             batch_size=batch_size,
#             work_center=work_center,
#             custom_fields=custom_fields,
#         )

#         instance.full_clean()
#         instance.save(user=self.user)

#         # Create step
#         for step_dict in step:
#             self.microbatch_flow_step_service.create(
#                 microbatch_flow=instance,
#                 **step_dict,
#                 custom_fields=custom_fields,
#             )

#         return instance

#     @transaction.atomic
#     def update(self, instance: MicrobatchFlow, data: dict) -> MicrobatchFlow:
#         # check permissions for update microbatch rule
#         if not self.permission_service.check_for_permission("change_microbatchrule"):
#             raise PermissionDenied()

#         fields = [
#             "item_name",
#             "batch_size",
#             "work_center",
#             "custom_fields",
#         ]
#         instance, _ = model_update(
#             instance=instance, fields=fields, data=data, user=self.user
#         )

#         step = data.get("step", [])

#         if step:
#             self.microbatch_flow_step_service.create_or_update_step(
#                 step=step, instance=instance
#             )

#         return instance

#     @transaction.atomic
#     def delete(self, instance: MicrobatchFlow) -> None:
#         # check permissions for delete microbatch rule
#         if not self.permission_service.check_for_permission("delete_microbatchrule"):
#             raise PermissionDenied()

#         instance.delete()
#         return True
