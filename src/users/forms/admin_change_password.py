from django import forms
from django.forms import ValidationError


class AdminChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
            },
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
            },
        ),
    )

    def clean(self):
        """
        Validate that new and confirmed passwords match.
        """
        new_password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return self.cleaned_data
