from django import forms

from .models import WeeklyShiftTemplate, OperationalException


class WeeklyShiftTemplateForm(forms.ModelForm):
    class Meta:
        model = WeeklyShiftTemplate
        fields = ["name", "external_id", "notes"]
        labels = {"name": "Weekly Shift Template Name", "external_id": "External ID", "notes": "Notes", "details": "Details"}
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "external_id": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            )
        }


class OperationalExceptionForm(forms.ModelForm):
    class Meta:
        model = OperationalException
        fields = ["external_id", 
                "notes", 
                "start_datetime", 
                "operational_exception_type", 
                "weekly_shift_template", 
                "resource"]
        labels = {"name": "Operational Exception Name", 
                "external_id": "External ID", 
                "notes": "Notes", 
                "start_datetime": "Start Datetime",
                "operational_exception_type": "Operational Exception Type",
                "weekly_shift_template": "Weekly Shift Template",
                "resource": "Resource"
                }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "external_id": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "start_datetime": forms.DateTimeInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "datetime-local",
                }
            ),
            "operational_exception_type": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "weekly_shift_template": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "resource": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }