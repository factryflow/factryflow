from django import forms

from job_manager.models import (
    Task,
    TaskType,
    WorkCenter,
)

from resource_assigner.models import AssignmentConstraint


# -----------------------------------------------------------------------------
# WorkCenter Forms
# -----------------------------------------------------------------------------


class WorkCenterForm(forms.ModelForm):
    class Meta:
        model = WorkCenter
        fields = ["name", "notes"]
        labels = {
            "name": "Work Center Name",
            "notes": "Notes",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
        }


# ------------------------------------------------------------------------------
# Task Type Forms
# ------------------------------------------------------------------------------


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ["name", "notes"]
        labels = {
            "name": "Task Type Name",
            "notes": "Notes",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }


# ------------------------------------------------------------------------------
# Task Forms
# ------------------------------------------------------------------------------


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "job",
            "task_type",
            "setup_time",
            "duration",
            "quantity",
            "run_time_per_unit",
            "item",
            "predecessors",
            "task_status",
            "work_center",
            "dependencies",
            "notes",
        ]

        labels = {
            "name": "Task Name",
            "job": "Job",
            "notes": "Notes",
            "setup_time": "Setup Time",
            "duration": "Duration",
            "quantity": "Quantity",
            "run_time_per_unit": "Run Time Per Unit",
            "item": "Item",
            "task_type": "Task Type",
            "task_status": "Task Status",
            "work_center": "Work Center",
            "dependencies": "Dependencies",
            "predecessors": "Predecessors",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "job": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "setup_time": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "number",
                }
            ),
            "duration": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "number",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "number",
                }
            ),
            "run_time_per_unit": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 ",
                    "type": "number",
                }
            ),
            "item": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "task_type": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "task_status": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm disabled:bg-gray-100 disabled:cursor-not-allowed rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit",
                    "disabled": "disabled",
                    "readonly": "readonly",
                }
            ),
            "work_center": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "dependencies": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "predecessors": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }


# ------------------------------------------------------------------------------
# Task Assignment Constraint Forms
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
            "assignment_rule",
        ]
        labels = {
            "task": "Task",
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
