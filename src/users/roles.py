from rolepermissions.roles import AbstractUserRole
from .utils import get_all_permissions

def get_all_avilable_permissions():
    # to get all permissions from django.contrib.auth.models.Permission
    data_dict = {permission: True for permission in get_all_permissions()}
    return data_dict

class Admin(AbstractUserRole):
    # admin has all permissions
    available_permissions = get_all_avilable_permissions()


class Operator(AbstractUserRole):
    # permissions = get_all_permissions()
    available_permissions = get_all_avilable_permissions()


class Planner(AbstractUserRole):
    # planner should have all permissions except user management
    available_permissions = {}
    permissions = get_all_permissions()
    for permission in permissions:
        if not permission.startswith("user"):
            available_permissions[permission] = True


class ReadOnly(AbstractUserRole):
    # to get only view acces from all permissions
    available_permissions = {}
    permissions = get_all_permissions()
    for permission in permissions:
        if permission.startswith("view") and not permission.startswith("user"):
            available_permissions[permission] = True
