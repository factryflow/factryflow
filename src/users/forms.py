from django import forms

from users.models import User

# ------------------------------------------------------------------------------
# User Forms
# ------------------------------------------------------------------------------


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "groups",
            "is_active",
        ]

        labels = {
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "groups": "Roles",
            "is_active": "Active",
        }

        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "groups": forms.SelectMultiple(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }
