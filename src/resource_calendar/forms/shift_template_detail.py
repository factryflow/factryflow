from django import forms

from resource_calendar.models import WeeklyShiftTemplateDetail

# ------------------------------------------------------------
#  WeeklyShiftTemplateDetailForm
# ------------------------------------------------------------


class WeeklyShiftTemplateDetailForm(forms.ModelForm):
    class Meta:
        model = WeeklyShiftTemplateDetail
        fields = ["weekly_shift_template", "day_of_week", "start_time", "end_time"]
        labels = {
            "weekly_shift_template": "Weekly Shift Template",
            "day_of_week": "Day of Week",
            "start_time": "Start Time",
            "end_time": "End Time",
        }
        widgets = {
            "weekly_shift_template": forms.Select(
                attrs={
                    "class": "mb-3 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "required": "required",
                }
            ),
            "day_of_week": forms.Select(
                attrs={
                    "class": "mb-3 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "required": "required",
                }
            ),
            "start_time": forms.TimeInput(
                attrs={
                    "class": "mb-3 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "time",
                    "required": "required",
                }
            ),
            "end_time": forms.TimeInput(
                attrs={
                    "class": "mb-5 border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                    "type": "time",
                    "required": "required",
                }
            ),
        }
