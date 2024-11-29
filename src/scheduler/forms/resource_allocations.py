from django import forms

from scheduler.models import ResourceAllocations


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
