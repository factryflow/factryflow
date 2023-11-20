from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Define paths that don't require authentication
        exempt_paths = [
            reverse("account_login"),
            reverse("account_signup"),
            reverse("account_reset_password"),
            reverse("account_reset_password_done"),
        ]

        # Skip middleware for exempt paths
        if request.path in exempt_paths or request.user.is_authenticated:
            return None

        # Use login_required for other views
        return login_required(view_func)(request, *view_args, **view_kwargs)
