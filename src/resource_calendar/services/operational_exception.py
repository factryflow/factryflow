from datetime import datetime

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.db import transaction
from resource_manager.models import Resource

from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
)


# -----------------------------------------------------------------------------
# OperationalExceptionTypeService
# -----------------------------------------------------------------------------


class OperationalExceptionTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        custom_fields: dict = None,
    ) -> OperationalExceptionType:
        # check for permissions for add operational exception type
        if not self.permission_service.check_for_permission(
            "add_operationalexceptiontype"
        ):
            raise PermissionDenied()

        exception_type = OperationalExceptionType.objects.create(
            name=name, external_id=external_id, notes=notes, custom_fields=custom_fields
        )
        exception_type.full_clean()
        exception_type.save(user=self.user)

        return exception_type

    @transaction.atomic
    def update(
        self, exception_type: OperationalExceptionType, data: dict
    ) -> OperationalExceptionType:
        # check for permissions for change operational exception type
        if not self.permission_service.check_for_permission(
            "change_operationalexceptiontype"
        ):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "custom_fields",
        ]

        exception_type, _ = model_update(
            instance=exception_type,
            fields=fields,
            data=data,
            user=self.user,
        )

        return exception_type

    @transaction.atomic
    def delete(self, exception_type: OperationalExceptionType) -> None:
        # check for permissions for delete operational exception type
        if not self.permission_service.check_for_permission(
            "delete_operationalexceptiontype"
        ):
            raise PermissionDenied()

        exception_type.delete()
        return True


# -----------------------------------------------------------------------------
# OperationalExceptionService
# -----------------------------------------------------------------------------


class OperationalExceptionService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        resource: Resource,
        start_datetime: datetime,
        end_datetime: datetime,
        operational_exception_type: OperationalExceptionType,
        weekly_shift_template: WeeklyShiftTemplate = None,
        external_id: str = "",
        notes="",
        custom_fields: dict = None,
    ) -> OperationalException:
        # check for permissions for add operational exception
        if not self.permission_service.check_for_permission("add_operationalexception"):
            raise PermissionDenied()

        exception = OperationalException.objects.create(
            resource=resource,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            operational_exception_type=operational_exception_type,
            weekly_shift_template=weekly_shift_template,
            external_id=external_id,
            notes=notes,
            custom_fields=custom_fields,
        )

        exception.full_clean()
        exception.save(user=self.user)

        return exception

    @transaction.atomic
    def update(
        self, exception: OperationalException, data: dict
    ) -> OperationalException:
        # check for permissions for change operational exception
        if not self.permission_service.check_for_permission(
            "change_operationalexception"
        ):
            raise PermissionDenied()

        fields = [
            "resource",
            "start_datetime",
            "end_datetime",
            "operational_exception_type",
            "weekly_shift_template",
            "external_id",
            "notes",
            "custom_fields",
        ]

        exception, _ = model_update(
            instance=exception,
            fields=fields,
            data=data,
            user=self.user,
        )

        return exception

    @transaction.atomic
    def delete(self, exception: OperationalException) -> None:
        # check for permissions for delete operational exception
        if not self.permission_service.check_for_permission(
            "delete_operationalexception"
        ):
            raise PermissionDenied()

        exception.delete()
        return True
