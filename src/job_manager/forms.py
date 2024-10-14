from django import forms

from .models import (
    Dependency,
    DependencyType,
    Item,
    Job,
    JobType,
    Task,
    TaskType,
    WorkCenter,
)

from resource_assigner.models import AssignmentConstraint


# ------------------------------------------------------------------------------
# Job Forms
# ------------------------------------------------------------------------------


class JobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = ["name", "notes"]
        labels = {
            "name": "Job Type Name",
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


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "name",
            "job_type",
            "description",
            "job_status",
            "customer",
            "dependencies",
            "notes",
            "due_date",
        ]
        labels = {
            "name": "Job Name",
            "dependencies": "Dependencies",
            "description": "Job Description",
            "notes": "Notes",
            "customer": "Customer",
            "job_type": "Job Type",
            "due_date": "Due Date",
            "job_status": "Job Status",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "dependencies": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "customer": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "due_date": forms.DateInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "date",
                }
            ),
            "job_type": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "job_status": forms.Select(
                attrs={
                    "class": "pointer-events-none cursor-not-allowed border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }


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
# Task Forms
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
                    "class": "pointer-events-none cursor-not-allowed border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
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





# ------------------------------------------------------------------------------
# Dependency Forms
# ------------------------------------------------------------------------------


class DependencyTypeForm(forms.ModelForm):
    class Meta:
        model = DependencyType
        fields = ["name", "notes"]
        labels = {
            "name": "Dependency Type Name",
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


class DependencyForm(forms.ModelForm):
    class Meta:
        model = Dependency
        fields = [
            "name",
            "expected_close_datetime",
            "dependency_type",
            "dependency_status",
            "notes",
        ]
        labels = {
            "name": "Dependency Name",
            "expected_close_datetime": "Expected Close Date",
            "notes": "Notes",
            "dependency_type": "Dependency Type",
            "dependency_status": "Dependency Status",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "expected_close_datetime": forms.DateTimeInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "datetime-local",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "dependency_type": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "dependency_status": forms.Select(
                attrs={
                    "class": "pointer-events-none cursor-not-allowed border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }


# ------------------------------------------------------------------------------
# Work Center Forms
# ------------------------------------------------------------------------------


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
# Item Forms
# ------------------------------------------------------------------------------


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "notes"]
        labels = {
            "name": "Item Name",
            "description": "Description",
            "notes": "Notes",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "description": forms.Textarea(
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
