from django import forms

from microbatching.models import (
    MicrobatchRule,
)


class MicrobatchRuleForm(forms.ModelForm):
    class Meta:
        model = MicrobatchRule
        fields = [
            "item_name",
            "work_center",
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
            "item_name": "Item Name",
            "work_center": "Work Center",
            "batch_size": "Batch Size",
        }
        widgets = {
            "item_name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "work_center": forms.Select(
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