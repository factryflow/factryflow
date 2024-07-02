from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied

from users.models import User

# ------------------------------------------------------------------------------
# User Service
# ------------------------------------------------------------------------------


class UserService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    # TODO: Might be used with user invite feature
    # def create(
    #     self,
    #     first_name,
    #     last_name,
    #     email
    # ) -> User:
    #     # check permissions for add user
    #     if not self.permission_service.check_for_permission("add_user"):
    #         raise PermissionDenied()

    #     user = User.objects.create(
    #         email=email,
    #         first_name=first_name,
    #         last_name=last_name
    #     )

    #     user.full_clean()
    #     user.save()

    #     return user

    def update(self, instance: User, data: dict) -> User:
        # check permissions for update user
        if not self.permission_service.check_for_permission("change_user"):
            raise PermissionDenied()

        fields = ["first_name", "last_name", "groups", "is_active"]

        user, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return user

    def delete(self, instance: User) -> None:
        # check permissions for delete user
        if not self.permission_service.check_for_permission("delete_user"):
            raise PermissionDenied()

        instance.delete()
        return True
