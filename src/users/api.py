from rolepermissions.roles import assign_role, get_user_roles, remove_role
from ninja import Router  

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from users.schemas import RoleIn

from users.utils import is_superuser, get_all_permissions

router = Router(tags=["users_roles"])

@router.post("/assign_role")
# @is_superuser
def assign_role_to_user(request, payload: RoleIn):
    user = get_object_or_404(User, id=payload.user_id)
    try:
        assign_role(user, payload.name)
        return {"message": f"{payload.name} Role assigned"}
    except Exception as e:
        return {"message": str(e)}


@router.post("/remove_role")
# @is_superuser
def remove_role_from_user(request, payload: RoleIn):
    user = get_object_or_404(User, id=payload.user_id)
    try:
        remove_role(user, payload.name)
        return {"message": "Role removed"}
    except Exception as e:
        return {"message": str(e)}


@router.get("/permissions")
#@is_superuser
def get_all_avilable_permissions(request):
    permissions = get_all_permissions()
    return {"permissions": list(permissions)}
