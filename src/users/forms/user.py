from django import forms
from users.models import User
from common.forms import get_select_widget, get_multi_select_widget

# ------------------------------------------------------------------------------
# User Forms
# ------------------------------------------------------------------------------


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "groups",
            "require_password_change",
            "is_active",
        ]

        labels = {
            "username": "Username",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "groups": "Roles",
            "require_password_change": "Require Password Change on Login",
            "is_active": "Active",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
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
            "groups": get_multi_select_widget(User.groups.field.related_model),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "groups",
            "require_password_change",
            "is_active",
        ]

        labels = {
            "username": "Username",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "password": "Initial Password",
            "groups": "Roles",
            "require_password_change": "Require Password Change on Login",
            "is_active": "Active",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
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
            "password": forms.PasswordInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                },
            ),
            "groups": get_multi_select_widget(User.groups.field.related_model),
            "require_password_change": forms.CheckboxInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"
                }
            ),
        }

    def clean(self):
        """
        Validate that new and confirmed passwords match.
        """

        username = self.cleaned_data["username"]
        email = self.cleaned_data.get("email", None)

        if ("@" in username) and not email:
            self.cleaned_data["email"] = username

        return self.cleaned_data
