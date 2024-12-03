from django import forms
from common.forms import get_select_widget, get_multi_select_widget
from resource_manager.models import Resource
from resource_calendar.models import WeeklyShiftTemplate
from users.models import User

# ------------------------------------------------------------------------------
# Resource Forms
# ------------------------------------------------------------------------------


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "name",
            "resource_type",
            "weekly_shift_template",
            "users",
            "notes",
        ]

        labels = {
            "name": "Resource Name",
            "resource_type": "Resource Type",
            "weekly_shift_template": "Weekly Shift Template",
            "users": "Users",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "resource_type": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "weekly_shift_template": get_select_widget(WeeklyShiftTemplate),
            "users": get_multi_select_widget(User),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }
