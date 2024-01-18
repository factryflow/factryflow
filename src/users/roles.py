from rolepermissions.roles import AbstractUserRole
from .utils import get_all_permissions, get_view_only_permissions, get_all_avilable_permissions


class Admin(AbstractUserRole):
    """
    Custom user role class for administrators.

    This class extends AbstractUserRole and provides all available permissions
    to users with the 'Admin' role.
    """
    available_permissions = get_all_avilable_permissions()


class Operator(AbstractUserRole):
    """
    Custom user role class for operators.

    This class extends AbstractUserRole and provides only view permissions
    for resources associated with the operator (customize as needed).
    """
    available_permissions = get_view_only_permissions()
    

class Planner(AbstractUserRole):
    """
    Custom user role class for planners.

    This class extends AbstractUserRole and provides all permissions
    except those related to user management.
    """
    available_permissions = {}
    permissions = get_all_permissions()

    for permission in permissions:
        if not permission.startswith("user"):
            available_permissions[permission] = True


class ReadOnly(AbstractUserRole):
    """
    Custom user role class for read-only access.

    This class extends AbstractUserRole and provides only view-related
    permissions (excluding those related to 'user').
    """
    available_permissions = get_view_only_permissions()
