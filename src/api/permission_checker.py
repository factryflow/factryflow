from functools import wraps
from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from rolepermissions.checkers import has_permission


def has_permission_decorator(operation_id):
    # Decorator function to check if the user has a specific permission.
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            """
            Wrapper function that checks if the user has the specified permission.

            Args:
                request (HttpRequest): The HTTP request object.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                HttpResponse: The result of the decorated view function.

            Raises:
                PermissionDenied: If the user does not have the specified permission.
            """
            if has_permission(request.user, operation_id):
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return wrapper

    return decorator


class AbstractPermissionService(ABC):
    """
    Abstract base class for services with permission-checking capabilities.
    """

    def __init__(self, user: User):
        """
        Args:
            operation_id (str): The operation ID of the permission to check.
        """
        self.user = user

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    def has_permission(self, operation_id):
        """
        Check if the user has the specified permission.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has the specified permission, False otherwise.
        """
        return has_permission(self.user, operation_id)
