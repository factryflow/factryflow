import re

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction

from users.models import User

# ------------------------------------------------------------------------------
# User Service
# ------------------------------------------------------------------------------


class UserService:
    def __init__(self, user, request_user=None) -> None:
        self.user = user
        if request_user:
            self.permission_service = AbstractPermissionService(user=request_user)
        else:
            self.permission_service = AbstractPermissionService(user=user)

    @staticmethod
    def _string_is_email(email_string):
        # Check if string is a valid email address.
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

        if re.fullmatch(regex, email_string):
            return True

        else:
            return False

    @transaction.atomic
    def create(self, *args, **kwargs) -> User:
        # check permissions for add user
        if not self.permission_service.check_for_permission("add_user"):
            raise PermissionDenied()

        groups = kwargs.pop("groups", [])
        username = kwargs["username"]

        if self._string_is_email(username) and not kwargs.get("email", None):
            kwargs["email"] = username

        user = User(**kwargs)

        user.full_clean()
        user.save()

        user.set_password(kwargs["password"])
        user.groups.set(groups)
        user.save()

        return user

    @transaction.atomic
    def update(self, instance: User, data: dict) -> User:
        # check permissions for update user
        if not self.permission_service.check_for_permission("change_user"):
            raise PermissionDenied()

        fields = [
            "first_name",
            "last_name",
            "groups",
            "is_active",
            "require_password_change",
        ]

        user, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return user

    @transaction.atomic
    def change_password(self, data: dict) -> User:
        if not self.permission_service.check_for_permission("change_user"):
            raise PermissionDenied()

        instance = self.user
        instance.set_password(data["new_password"])
        instance.require_password_change = False
        instance.save()

        return instance

    @transaction.atomic
    def delete(self, instance: User) -> None:
        # check permissions for delete user
        if not self.permission_service.check_for_permission("delete_user"):
            raise PermissionDenied()

        instance.delete()
        return True
