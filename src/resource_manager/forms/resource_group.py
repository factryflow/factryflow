from django import forms

from resource_manager.models import ResourceGroup


# ------------------------------------------------------------------------------
# ResourceGroup Forms
# ------------------------------------------------------------------------------


class ResourceGroupForm(forms.ModelForm):
    class Meta:
        model = ResourceGroup
        fields = ["name", "parent", "resources", "notes"]
        labels = {
            "name": "Resource Pool Name",
            "parent": "Select Parent Resource Pool",
            "resources": "Resources",
            "notes": "Notes",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "parent": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "resources": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
        }
