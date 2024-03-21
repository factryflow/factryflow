from django import forms

from .models import Resource, ResourcePool, WorkUnit

# ------------------------------------------------------------------------------
# Resource Forms
# ------------------------------------------------------------------------------

class ResourceForm(forms.ModelForm):
    
    class Meta:
        model = Resource
        fields = [
            "external_id",
            "name",
            "resource_type",
            "weekly_shift_template",
            "work_units",
            "users",
            "notes"
        ]

        labels = {
            "name": "Resource Name",
            "resource_type": "Resource Type",
            "weekly_shift_template": "Weekly Shift Template",
            "work_units": "Work Units",
            "users": "Users",
        }

        widgets = {
            "external_id": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
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
            "weekly_shift_template": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "work_units": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "users": forms.SelectMultiple(
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


# ------------------------------------------------------------------------------
# ResourcePool Forms
# ------------------------------------------------------------------------------

class ResourcePoolForm(forms.ModelForm):
    class Meta:
        model = ResourcePool
        fields = ["external_id", "name", "parent", "resources", "work_units", "notes"]
        labels = {
            "name": "Resource Pool Name",
            "external_id": "External ID",
            "parent": "Select Parent Resource Pool",
            "resources": "Resources",
            "work_units": "Work Units",
            "notes": "Notes",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "external_id": forms.TextInput(
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
            "work_units": forms.SelectMultiple(
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


# ------------------------------------------------------------------------------
# WorkUnit Forms
# ------------------------------------------------------------------------------

class WorkUnitForm(forms.ModelForm):
    class Meta:
        model = WorkUnit
        fields = ["external_id", "name", "notes"]
        labels = {
            "external_id": "External ID",
            "name": "Work Unit Name",
            "notes": "Notes",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "external_id": forms.TextInput(
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