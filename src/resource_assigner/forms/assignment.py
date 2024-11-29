from django import forms

from resource_assigner.models import TaskResourceAssigment


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
            "resources": "Resources",
        }
        widgets = {
            "task": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "resources": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }
