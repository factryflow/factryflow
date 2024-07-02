from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("home")
    template_name = "account/change_password.html"
