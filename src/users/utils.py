from functools import wraps

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.exceptions import PermissionDenied


def get_all_permissions():
    """
    Retrieve a set of all unique permission codenames available in the system,
    excluding permissions related to User, Permission, SocialAccount, Group,
    SocialApp, and SocialToken.

    Returns:
        set: A set containing unique permission codenames.

    Note:
        This function queries the ContentType model to identify content types for
        relevant models and excludes permissions associated with those content
        types from the final result.
    """
    permissions = set()

    try:
        # get content types for Group, Permission, SocialAccount, etc.

        permission_content_type = ContentType.objects.get_for_model(Permission)
        social_account_content_type = ContentType.objects.get_for_model(SocialAccount)

        group_content_type = ContentType.objects.get_for_model(Group)

        social_app_content_type = ContentType.objects.get_for_model(SocialApp)
        social_token_content_type = ContentType.objects.get_for_model(SocialToken)

        # exclude content types for User, Permission, SocialAccount, etc. from permissions
        excluded_content_types = Q(
            content_type__in=[
                permission_content_type,
                social_account_content_type,
                group_content_type,
                social_app_content_type,
                social_token_content_type,
            ]
        )

        # filtered permissions
        filtered_permissions = Permission.objects.exclude(excluded_content_types)

        # to get all permissions from django.contrib.auth.models.Permissions
        for permission in filtered_permissions.all():
            permissions.add(permission.codename)
        return permissions
    except Exception:
        return []


def is_superuser(func):
    """
    Decorator function to check if the user making the request is a superuser.

    Args:
        func (callable): The view function to be decorated.

    Returns:
        callable: The decorated view function.
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return wrapper


def get_all_avilable_permissions():
    """
    Retrieve all available permissions as a dictionary with True values.

    Returns:
    dict: A dictionary where keys are permission codenames, and values are set to True.
    """
    try:
        data_dict = {permission: True for permission in get_all_permissions()}
        return data_dict
    except Exception:
        return {}


def get_view_only_permissions():
    """
    Retrieve view-only permissions (excluding user-related views) as a dictionary with True values.

    Returns:
    dict: A dictionary where keys are permission codenames for view-only permissions, and values are set to True.
    """
    data_dict = {}
    try:
        permissions = get_all_permissions()
        for permission in permissions:
            if permission.startswith("view") and "user" not in permission:
                data_dict[permission] = True
        return data_dict
    except Exception:
        return {}
