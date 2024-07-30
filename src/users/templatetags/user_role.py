from django import template
from rolepermissions.roles import get_user_roles

register = template.Library()


@register.simple_tag
def get_current_user_role(user):
    """
    Returns the role of the current user.

    Parameters:
    - user: The user object for which to retrieve the role.

    Returns:
    - The name of the user's role, or None if the user has no roles.
    """
    roles = get_user_roles(user)
    if roles:
        return roles[0].name
    return None
