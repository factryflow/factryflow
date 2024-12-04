from django import forms
from common.forms import get_select_widget
from microbatching.models.microbatch_flow import (
    MicrobatchFlow,
    MicrobatchRule,
)


class MicrobatchFlowForm(forms.ModelForm):
    class Meta:
        model = MicrobatchFlow
        fields = [
            "name",
            "description",
            "start_rule",
            "end_rule",
            "min_flow_length",
            "max_flow_length",
            "batch_size",
        ]
        exclude = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "custom_fields",
        ]
        labels = {
            "name": "Name",
            "description": "Description",
            "start_rule": "Start Rule",
            "end_rule": "End Rule",
            "min_flow_length": "Min Flow Length",
            "max_flow_length": "Max Flow Length",
            "batch_size": "Batch Size",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "start_rule": get_select_widget(MicrobatchRule),
            "end_rule": get_select_widget(MicrobatchRule),
            "min_flow_length": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "max_flow_length": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "batch_size": forms.NumberInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }
