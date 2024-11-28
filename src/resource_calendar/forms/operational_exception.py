from django import forms

from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
)


# ------------------------------------------------------------
#  OperationalExceptionTypeForm
# ------------------------------------------------------------


class OperationalExceptionTypeForm(forms.ModelForm):
    class Meta:
        model = OperationalExceptionType
        fields = ["name", "notes"]
        labels = {
            "name": "Operational Exception Type Name",
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


# ------------------------------------------------------------
#  OperationalExceptionForm
# ------------------------------------------------------------


class OperationalExceptionForm(forms.ModelForm):
    class Meta:
        model = OperationalException
        fields = [
            "resource",
            "weekly_shift_template",
            "start_datetime",
            "end_datetime",
            "operational_exception_type",
            "notes",
        ]
        labels = {
            "name": "Operational Exception Name",
            "notes": "Notes",
            "start_datetime": "Start Datetime",
            "end_datetime": "End Datetime",
            "operational_exception_type": "Operational Exception Type",
            "weekly_shift_template": "Weekly Shift Template",
            "resource": "Resource",
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
            "start_datetime": forms.DateTimeInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "datetime-local",
                }
            ),
            "end_datetime": forms.DateTimeInput(
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
