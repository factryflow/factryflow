from django import forms

from resource_assigner.models import (
    AssignmentConstraint,
)


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
            "task",
        ]
        labels = {
            "assignment_rule": "Assignment Rule",
            "resource_group": "Resource Group",
            "resources": "Resources",
            "resource_count": "Resource Count",
            "use_all_resources": "Use All Resources",
        }
        widgets = {
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
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w/1-2 p-3 bg-inherit"
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
