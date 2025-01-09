from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from users.forms.user import UserProfileForm
from django.contrib.auth import update_session_auth_hash

class MyAccountView(LoginRequiredMixin, View):
    """
    View for displaying the My Account page with both profile and password change forms.
    """
    template_name = "account/my_account.html"

    def get(self, request):
        profile_form = UserProfileForm(instance=request.user, user=request.user)
        password_form = PasswordChangeForm(user=request.user)
        
        base_class = "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
        for field in password_form.fields.values():
            field.widget.attrs.update({
                "class": base_class
            })
        
        # Add Alpine.js bindings for password validation
        password_form.fields['new_password1'].widget.attrs.update({
            "x-model": "newPassword",
            "@input": "validatePasswords()"
        })
        password_form.fields['new_password2'].widget.attrs.update({
            "x-model": "confirmPassword",
            "@input": "validatePasswords()"
        })
        
        return render(request, self.template_name, {
            "profile_form": profile_form,
            "password_form": password_form
        })

class UpdateProfileView(LoginRequiredMixin, View):
    """
    Handle user profile updates (first name, last name).
    """
    template_name = "account/my_account.html"

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            try:
                # Only update first_name and last_name
                user = request.user
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.save(update_fields=["first_name", "last_name"])
                
                messages.success(request, "Profile updated successfully!")
                return redirect('users:my_account')
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
        
        # Re-render the form with errors and preserved data
        password_form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {
            "profile_form": form,
            "password_form": password_form
        })

class ChangePasswordView(PasswordChangeView):
    """
    Handle password changes.
    """
    form_class = PasswordChangeForm
    template_name = "account/my_account.html"
    success_url = reverse_lazy("users:my_account")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        base_class = "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
        for field in form.fields.values():
            field.widget.attrs.update({
                "class": base_class
            })
            
        # Alpine.js bindings for password validation
        form.fields['new_password1'].widget.attrs.update({
            "x-model": "newPassword",
            "@input": "validatePasswords()"
        })
        form.fields['new_password2'].widget.attrs.update({
            "x-model": "confirmPassword",
            "@input": "validatePasswords()"
        })
        return form

    def form_valid(self, form):
        try:
            form.save()
            update_session_auth_hash(self.request, form.user)
            
            messages.success(self.request, "Password changed successfully!")
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, f"Error changing password: {str(e)}")
            return redirect('users:my_account')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect('users:my_account')
