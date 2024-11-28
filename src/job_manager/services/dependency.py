from datetime import datetime

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction

from job_manager.models import (
    Dependency,
    DependencyType,
)


# ------------------------------------------------------------------------------
# Dependency Type Services
# ------------------------------------------------------------------------------


class DependencyTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        custom_fields: dict = None,
    ) -> DependencyType:
        # check for permission to create dependency type
        if not self.permission_service.check_for_permission("add_dependencytype"):
            raise PermissionDenied()

        dependency_type = DependencyType.objects.create(
            name=name, external_id=external_id, notes=notes, custom_fields=custom_fields
        )
        dependency_type.full_clean()
        dependency_type.save(user=self.user)

        return dependency_type

    @transaction.atomic
    def update(self, dependency_type: DependencyType, data: dict) -> DependencyType:
        # check for permission to update dependency type
        if not self.permission_service.check_for_permission("change_dependencytype"):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "custom_fields",
        ]

        dependency_type, _ = model_update(
            instance=dependency_type,
            fields=fields,
            data=data,
            user=self.user,
        )

        return dependency_type

    @transaction.atomic
    def delete(self, dependency_type: DependencyType) -> None:
        # check for permission to delete dependency type
        if not self.permission_service.check_for_permission("delete_dependencytype"):
            raise PermissionDenied()

        dependency_type.delete()
        return True


# ------------------------------------------------------------------------------
# Dependency Services
# ------------------------------------------------------------------------------


class DependencyService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        name: str,
        dependency_type: DependencyType,
        dependency_status: str = "PD",
        expected_close_datetime: datetime = None,
        notes: str = "",
        external_id: str = "",
        custom_fields: dict = None,
    ) -> Dependency:
        # check for permission to create dependency
        if not self.permission_service.check_for_permission("add_dependency"):
            raise PermissionDenied()

        dependency = Dependency.objects.create(
            name=name,
            dependency_type=dependency_type,
            expected_close_datetime=expected_close_datetime,
            notes=notes,
            dependency_status=dependency_status,
            external_id=external_id,
            custom_fields=custom_fields,
        )

        dependency.full_clean()
        dependency.save(user=self.user)

        return dependency

    @transaction.atomic
    def update(self, instance: Dependency, data: dict) -> Dependency:
        # check for permission to update dependency
        if not self.permission_service.check_for_permission("change_dependency"):
            raise PermissionDenied()

        fields = [
            "name",
            "dependency_type",
            "dependency_status",
            "expected_close_datetime",
            "actual_close_datetime",
            "notes",
            "external_id",
            "custom_fields",
        ]

        dependency, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        return dependency

    @transaction.atomic
    def delete(self, instance: Dependency) -> None:
        # check for permission to delete dependency
        if not self.permission_service.check_for_permission("delete_dependency"):
            raise PermissionDenied()

        instance.delete()
        return True
