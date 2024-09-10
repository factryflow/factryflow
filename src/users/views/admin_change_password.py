from common.utils.views import add_notification_headers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.edit import FormView
from users.forms.admin_change_password import AdminChangePasswordForm
from users.models import User
from users.services import UserService


class AdminChangePasswordView(FormView):
    """
    Handle POST request to create or update a model instance using Django form and service.

    Args:
        request: The HTTP request object.
        id: The ID of the model instance (optional).

    Returns:
        The response indicating success or failure of the operation.
    """
    template_name = "account/admin_change_password.html"
    form_class = AdminChangePasswordForm

    def post(self, request, id):
        form = self.get_form()

        if len(form.errors) > 0:
            form_errors = []
            for _, errors in form.errors.items():
                for error in errors:
                    form_errors.append({
                        "type": "error",
                        "success": False,
                        "message": error,
                    })
            return render(self.request, self.template_name, {"form": form, "form_errors": form_errors})

        if form.is_valid():
            user = get_object_or_404(User, id=id)

            user_service = UserService(user)
            user_service.change_password(data=request.POST)

            response = redirect(reverse("users:view_users", args=[id]))

            add_notification_headers(
                response,
                "Password has been changed.",
                "success",
            )

            if request.htmx:
                headers = {"HX-Redirect": reverse("users:view_users", args=[id])}
                response = HttpResponse(status=204, headers=headers)

            return response

        else:
            return render(
                request,
                self.template_name,
                {"form": form},
            )
