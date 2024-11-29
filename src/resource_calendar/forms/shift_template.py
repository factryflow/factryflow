from django import forms

from resource_calendar.models import WeeklyShiftTemplate


# ------------------------------------------------------------
#  WeeklyShiftTemplateForm
# ------------------------------------------------------------


class WeeklyShiftTemplateForm(forms.ModelForm):
    class Meta:
        model = WeeklyShiftTemplate
        fields = [
            "name",
            "notes",
            "description",
        ]
        labels = {
            "name": "Weekly Shift Template Name",
            "notes": "Notes",
            "description": "Description",
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
            "description": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }
