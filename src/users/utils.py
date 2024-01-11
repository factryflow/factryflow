from functools import wraps
from http import HTTPStatus

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


def get_all_permissions():
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


# decorator to check if user is superuser or not
def is_superuser(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return {
                "message": "PermissionDenied",
                "detail": "User is not superuser",
                "status": HTTPStatus.FORBIDDEN,
            }

    return wrapper
