from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Define view names that don't require authentication
        exempt_view_names = (
            "account_login",
            "account_signup",
            "account_reset_password",
            "account_reset_password_done",
        )

        # Define paths that should bypass the login requirement
        exempt_paths = ("/api/",)

        # Convert view names to URLs
        exempt_urls = [reverse(view_name) for view_name in exempt_view_names]

        # Skip middleware for exempt paths and any path starting with /api/
        if any(request.path_info.startswith(path) for path in exempt_urls + list(exempt_paths)) or request.user.is_authenticated:
            return None

        # Use login_required for other views
        return login_required(view_func)(request, *view_args, **view_kwargs)
