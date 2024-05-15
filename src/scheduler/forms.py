from django import forms

from .models import SchedulerRuns, ResourceAllocations, ResourceIntervals


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


class ResourceIntervalsForm(forms.ModelForm):
    class Meta:
        model = ResourceIntervals
        fields = ["resource", "task", "interval_start", "interval_end"]
        labels = {
            "resource": "Resource",
            "task": "Task",
            "interval_start": "Interval Start",
            "interval_end": "Interval End",
        }
        widgets = {
            "resource": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "task": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "interval_start": forms.DateTimeInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "interval_end": forms.DateTimeInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }


class ResourceAllocationsForm(forms.ModelForm):
    class Meta:
        model = ResourceAllocations
        fields = ["resource", "task"]
        labels = {
            "resource": "Resource",
            "task": "Task",
        }
        widgets = {
            "resource": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "task": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }
