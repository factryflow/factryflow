from django import forms

from scheduler.models import SchedulerRuns


class SchedulerRunsForm(forms.ModelForm):
    class Meta:
        model = SchedulerRuns
        fields = ["start_time", "end_time", "details", "status"]
        labels = {
            "start_time": "Start Time",
            "end_time": "End Time",
            "details": "Details",
            "status": "Status",
        }
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "details": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "pointer-events-none cursor-not-allowed border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }
