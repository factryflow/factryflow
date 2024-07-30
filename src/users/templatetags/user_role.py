from django import template
from rolepermissions.roles import get_user_roles

register = template.Library()


@register.simple_tag
def get_current_user_role(user):
    """
    Returns the role of the current user.

    Args:
        user (User): The user object for which to retrieve the role.

    Returns:
        str: The name of the user's role, or "Normal User" if the user has no roles.
    """
    user_role = "Normal"

    if user.is_superuser:
        user_role = "Super Admin"
    elif user.is_staff:
        user_role = "Staff"
    else:
        roles = get_user_roles(user)
        if roles:
            user_role = roles[0].name

    return user_role
