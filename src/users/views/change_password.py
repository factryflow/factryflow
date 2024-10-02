from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render

from django.http import HttpResponseServerError


class ChangePasswordView(PasswordChangeView):
    """
    Handle POST request to create or update a model instance using Django form and service.

    Args:
        request: The HTTP request object.
        id: The ID of the model instance (optional).

    Returns:
        The response indicating success or failure of the operation.
    """

    form_class = PasswordChangeForm
    success_url = reverse_lazy("dashboard", kwargs={"home": "true", "gantt_type": "job"})
    template_name = "account/change_password.html"

    def post(self, *args, **kwargs):
        try:
            form = self.get_form()

            if form.is_valid():
                # if form is valid, update the user's password and redirect to success_url
                user = self.request.user
                user.require_password_change = False
                user.save()

                return super().post(*args, **kwargs)
            else:
                # if form is invalid, capture errors
                form_errors = []
                for _, errors in form.errors.items():
                    for error in errors:
                        form_errors.append(
                            {
                                "type": "error",
                                "success": False,
                                "message": error,
                            }
                        )
                return render(
                    self.request,
                    self.template_name,
                    {"form": form, "form_errors": form_errors},
                )

        except Exception as e:
            return HttpResponseServerError("Internal Server Error")
