from common.utils.services import get_model_fields
from django import forms

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
)


# ------------------------------------------------------------------------------
# AssigmentRule Forms
# ------------------------------------------------------------------------------


class AssigmentRuleForm(forms.ModelForm):
    class Meta:
        model = AssigmentRule
        fields = [
            "name",
            "work_center",
            "notes",
            "description",
            "is_active",
        ]
        exclude = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "custom_fields",
        ]
        labels = {
            "name": "Name",
            "work_center": "Work Center",
            "is_active": "Is Active",
            "notes": "Notes",
            "description": "Description",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "work_center": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w/1-2 p-3",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
        }


# ------------------------------------------------------------------------------
# AssigmentRuleCriteria Forms
# ------------------------------------------------------------------------------


class AssigmentRuleCriteriaForm(forms.ModelForm):
    class Meta:
        model = AssigmentRuleCriteria
        fields = "__all__"
        exclude = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "custom_fields",
        ]
        labels = {
            "assigment_rule": "Assigment Rule",
            "field": "Field",
            "operator": "Operator",
            "value": "Value",
        }
        widgets = {
            "assigment_rule": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "field": forms.Select(
                choices=get_model_fields(
                    "Task", "job_manager", ["item", "task_type", "job", "work_center"]
                ),
                attrs={
                    "class": "mb-3 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                },
            ),
            "operator": forms.Select(
                attrs={
                    "class": "mb-3 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "value": forms.TextInput(
                attrs={
                    "class": "mb-5 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }


# ------------------------------------------------------------------------------
# AssigmentRuleCriteria, AssigmentRule model formset
# ------------------------------------------------------------------------------

AssigmentRuleCriteriaFormSet = forms.inlineformset_factory(
    AssigmentRule,
    AssigmentRuleCriteria,
    form=AssigmentRuleCriteriaForm,
    extra=2,
    can_delete=False,
)
