# from django import forms

# from microbatching.models.microbatch_rule import (
#     MicrobatchRule,
#     MicrobatchRuleCriteria,
# )
# from microbatching.utils import get_model_fields


# class MicrobatchRuleForm(forms.ModelForm):
#     class Meta:
#         model = MicrobatchRule
#         fields = [
#             "item_name",
#             "work_center",
#             "batch_size",
#         ]
#         exclude = [
#             "created_by",
#             "updated_by",
#             "created_at",
#             "updated_at",
#             "custom_fields",
#         ]
#         labels = {
#             "item_name": "Item Name",
#             "work_center": "Work Center",
#             "batch_size": "Batch Size",
#         }
#         widgets = {
#             "item_name": forms.TextInput(
#                 attrs={
#                     "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
#                 }
#             ),
#             "work_center": forms.Select(
#                 attrs={
#                     "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
#                 }
#             ),
#             "batch_size": forms.NumberInput(
#                 attrs={
#                     "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
#                 }
#             ),
#         }


# class MicrobatchRuleCriteriaForm(forms.ModelForm):
#     class Meta:
#         model = MicrobatchRuleCriteria
#         fields = "__all__"
#         exclude = [
#             "created_by",
#             "updated_by",
#             "created_at",
#             "updated_at",
#             "custom_fields",
#         ]
#         labels = {
#             "microbatch_rule": "Microbatch Rule",
#             "field": "Field",
#             "operator": "Operator",
#             "value": "Value",
#         }
#         widgets = {
#             "assigment_rule": forms.Select(
#                 attrs={
#                     "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
#                 }
#             ),
#             "field": forms.Select(
#                 choices=get_model_fields(
#                     "Task", "job_manager", ["item", "task_type", "job", "work_center"]
#                 ),
#                 attrs={
#                     "class": "mb-3 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
#                 },
#             ),
#             "operator": forms.Select(
#                 attrs={
#                     "class": "mb-3 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
#                 }
#             ),
#             "value": forms.TextInput(
#                 attrs={
#                     "class": "mb-5 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
#                 }
#             ),
#         }
