from django import forms

from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    TaskResourceAssigment,
)
from resource_assigner.utils import get_model_fields

# ------------------------------------------------------------------------------
# TaskResource Assignment Forms
# ------------------------------------------------------------------------------


class TaskResourceAssigmentForm(forms.ModelForm):
    class Meta:
        model = TaskResourceAssigment
        fields = "__all__"
        exclude = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "custom_fields",
        ]
        labels = {
            "task": "Task",
            "assigment_rule": "Assigment Rule",
            "resource": "Resource",
        }
        widgets = {
            "task": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "assigment_rule": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "resource": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }


# ------------------------------------------------------------------------------
# AssigmentRule Forms
# ------------------------------------------------------------------------------


class AssigmentRuleForm(forms.ModelForm):
    class Meta:
        model = AssigmentRule
        fields = [
            "external_id",
            "name",
            "work_center",
            "is_active",
            "notes",
            "description",
        ]
        exclude = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "custom_fields",
        ]
        labels = {
            "external_id": "External ID",
            "name": "Name",
            "work_center": "Work Center",
            "is_active": "Is Active",
            "notes": "Notes",
            "description": "Description",
        }
        widgets = {
            "external_id": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
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
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
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
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                },
            ),
            "operator": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "value": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }


# ------------------------------------------------------------------------------
# AssignmentConstraint Forms
# ------------------------------------------------------------------------------


class AssignmentConstraintForm(forms.ModelForm):
    class Meta:
        model = AssignmentConstraint
        fields = "__all__"
        exclude = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "custom_fields",
        ]
        labels = {
            "task": "Task",
            "assignment_rule": "Assignment Rule",
            "resource_group": "Resource Group",
            "resources": "Resources",
            "resource_count": "Resource Count",
            "use_all_resources": "Use All Resources",
        }
        widgets = {
            "task": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "assignment_rule": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "resource_group": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "resources": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "resource_count": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "use_all_resources": forms.CheckboxInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }

    def clean(self, *args, **kwargs):
        resource_group_set = self.cleaned_data.get("resource_group") is not None
        resources_set = self.cleaned_data.get("resources").count() > 0

        if resource_group_set and resources_set:
            raise forms.ValidationError(
                "You cannot set both resource_group and resources. Choose one."
            )
        elif not resource_group_set and not resources_set:
            raise forms.ValidationError(
                "You must set either resource_group or resources."
            )

        # ensure that either task or assignment_rule is set
        if not (self.cleaned_data.get("task")) and not (
            self.cleaned_data.get("assignment_rule")
        ):
            raise forms.ValidationError("task or assignment_rule must be set.")

        if self.cleaned_data.get("task") and self.cleaned_data.get("assignment_rule"):
            raise forms.ValidationError(
                "Assignment constraints directly assigned to tasks cannot have assignment rules."
            )
