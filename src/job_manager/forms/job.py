from django import forms
from common.forms import get_multi_select_widget, get_select_widget
from job_manager.models import (
    Job,
    JobType,
    Dependency,
)

# ------------------------------------------------------------------------------
# Job Type Forms
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


# ------------------------------------------------------------------------------
# Job Forms
# ------------------------------------------------------------------------------


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
            "manual_priority",
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
            "manual_priority": "Manual Priority",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "dependencies": get_multi_select_widget(Dependency),
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
            "job_type": get_select_widget(JobType),
            "job_status": forms.Select(
                attrs={
                    "class": "pointer-events-none cursor-not-allowed border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "manual_priority": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "number",
                }
            ),
        }
