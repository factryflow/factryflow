from functools import wraps

from django.core.exceptions import PermissionDenied
from rolepermissions.checkers import has_permission


def has_permission_decorator(operation_id):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if has_permission(request.user, operation_id):
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return wrapper

    return decorator
