from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router
from rolepermissions.roles import assign_role, remove_role

from users.schemas import RoleIn
from users.utils import get_all_permissions, is_superuser

router = Router(tags=["users_roles"])


@router.post("/assign_role")
@is_superuser
def assign_role_to_user(request, payload: RoleIn):
    """
    Summary:
    --------
        Assign a role to a user.

    Args:
    -----
        request (HttpRequest): The HTTP request object.
        payload (RoleIn): The payload containing user_id and name of the role.

    Returns:
    --------
        dict: A dictionary containing a success message if the role is assigned, or an error message if unsuccessful.

    Raises:
    -------
        HTTPException: If the user is not found or if there is an error assigning the role.
    """
    user = get_object_or_404(settings.AUTH_USER_MODEL, id=payload.user_id)
    try:
        assign_role(user, payload.name)
        return {"message": f"{payload.name.name} Role assigned"}
    except Exception as e:
        return {"message": str(e)}


@router.post("/remove_role")
@is_superuser
def remove_role_from_user(request, payload: RoleIn):
    """
    Summary:
    --------
        Remove a role from a user.

    Args:
    -----
        request (HttpRequest): The HTTP request object.
        payload (RoleIn): The payload containing user_id and name of the role.

    Returns:
    --------
        dict: A dictionary containing a success message if the role is removed, or an error message if unsuccessful.

    Raises:
    -------
        HTTPException: If the user is not found or if there is an error removing the role.
    """
    user = get_object_or_404(settings.AUTH_USER_MODEL, id=payload.user_id)
    try:
        remove_role(user, payload.name)
        return {"message": "Role removed"}
    except Exception as e:
        return {"message": str(e)}


@router.get("/permissions")
@is_superuser
def get_all_avilable_permissions(request):
    """
    Summary:
    --------
        Get a list of all available permissions.

    Args:
    -----
        request (HttpRequest): The HTTP request object.

    Returns:
    --------
        dict: A dictionary containing a list of all available permissions.
    """
    permissions = get_all_permissions()
    return {"permissions": list(permissions)}
