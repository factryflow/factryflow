from collections import defaultdict
from datetime import datetime, time

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from resource_manager.models import Resource

from .models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)


# -----------------------------------------------------------------------------
# WeeklyShiftTemplateDetailService
# -----------------------------------------------------------------------------


class WeeklyShiftTemplateDetailService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    def _parse_time(self, time_input: str | time) -> datetime.time:
        """
        Parse a time string (expected in %H:%M format) and return a time object.
        """
        if isinstance(time_input, time):
            time_input = time_input.strftime("%H:%M")
        try:
            return datetime.strptime(time_input, "%H:%M").time()
        except ValueError:
            raise ValidationError(
                f"Invalid time format: '{time_input}'. Expected format HH:MM."
            )

    @transaction.atomic
    def create(
        self,
        day_of_week: int,
        start_time: str | time,
        end_time: str | time,
    ) -> WeeklyShiftTemplateDetail:
        """
        Create a WeeklyShiftTemplateDetail.
        """
        # check for permissions for add weekly shift template detail
        if not self.permission_service.check_for_permission(
            "add_weeklyshifttemplatedetail"
        ):
            raise PermissionDenied()

        weekly_shift_template_detail = WeeklyShiftTemplateDetail.objects.create(
            day_of_week=day_of_week,
            start_time=self._parse_time(start_time),
            end_time=self._parse_time(end_time),
        )

        weekly_shift_template_detail.full_clean()
        weekly_shift_template_detail.save(user=self.user)

        return weekly_shift_template_detail

    @transaction.atomic
    def create_bulk(
        self,
        details: list[dict],
    ) -> None:
        """
        Create a list of WeeklyShiftTemplateDetails.
        """
        # check for permissions for add weekly shift template detail
        if not self.permission_service.check_for_permission(
            "add_weeklyshifttemplatedetail"
        ):
            raise PermissionDenied()

        for detail_data in details:
            self.create(
                day_of_week=detail_data["day_of_week"],
                start_time=detail_data["start_time"],
                end_time=detail_data["end_time"],
            )

    @transaction.atomic
    def update(
        self,
        instance: WeeklyShiftTemplateDetail,
        data: dict,
    ) -> WeeklyShiftTemplateDetail:
        """
        Update a WeeklyShiftTemplateDetail.
        """
        # check for permissions for change weekly shift template detail
        if not self.permission_service.check_for_permission(
            "change_weeklyshifttemplatedetail"
        ):
            raise PermissionDenied()

        fields = [
            "day_of_week",
            "start_time",
            "end_time",
        ]

        weekly_shift_template_detail, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        weekly_shift_template_detail.full_clean()
        weekly_shift_template_detail.save(user=self.user)

        return weekly_shift_template_detail

    @transaction.atomic
    def delete(self, instance: WeeklyShiftTemplateDetail) -> None:
        """
        Delete a WeeklyShiftTemplateDetail.
        """
        # check for permissions for delete weekly shift template detail
        if not self.permission_service.check_for_permission(
            "delete_weeklyshifttemplatedetail"
        ):
            raise PermissionDenied()

        instance.delete()
        return True


# -----------------------------------------------------------------------------
# WeeklyShiftTemplateService
# -----------------------------------------------------------------------------


class WeeklyShiftTemplateService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

        self.weeklyshifttemplatedetailservice = WeeklyShiftTemplateDetailService(
            user=user
        )

    def _process_details(
        self, template: WeeklyShiftTemplate, new_details: list[dict]
    ) -> None:
        """
        Process a list of WeeklyShiftTemplateDetails for a given WeeklyShiftTemplate.
        """
        existing_details = template.weekly_shift_template_details.all()

        # Convert existing details to a dictionary
        existing_detail_dict = {
            (detail.day_of_week, detail.start_time, detail.end_time): detail
            for detail in existing_details
        }

        # Convert new details to a dictionary
        new_detail_dict = {
            (d["day_of_week"], d["start_time"], d["end_time"]): d for d in new_details
        }
        # Determine details to create and delete
        details_to_create = [
            detail
            for key, detail in new_detail_dict.items()
            if key not in existing_detail_dict
        ]

        details_to_delete = [
            detail
            for key, detail in existing_detail_dict.items()
            if key not in new_detail_dict
        ]

        # Delete old details
        for detail in details_to_delete:
            self.weeklyshifttemplatedetailservice.delete(detail)

        # Create new details
        self.weeklyshifttemplatedetailservice.create_bulk(details=details_to_create)

    def _check_no_overlapping_details(self, template: WeeklyShiftTemplate) -> None:
        details_by_day = defaultdict(list)

        # Group details by day of the week
        for detail in template.weekly_shift_template_details.all():
            details_by_day[detail.day_of_week].append(detail)

        # Check for overlaps within each day, but only if there's more than one detail for that day
        for day, details in details_by_day.items():
            if len(details) > 1:
                self._check_overlaps_for_single_day(details)

    def _check_overlaps_for_single_day(self, details) -> None:
        details.sort(key=lambda d: d.start_time)  # Sort by start time

        for i in range(len(details) - 1):
            if details[i].end_time > details[i + 1].start_time:
                raise ValidationError(
                    f"Details overlap on day {details[i].day_of_week}: Detail {details[i].id} overlaps with Detail {details[i + 1].id}"
                )

    def _validate_details_fields(self, details):
        required_keys = {"day_of_week", "start_time", "end_time"}
        for detail in details:
            missing_keys = required_keys - detail.keys()
            if missing_keys:
                raise ValueError(
                    f"Detail is missing required keys: {', '.join(missing_keys)}"
                )

    @transaction.atomic
    def create(
        self,
        name: str,
        external_id: str = "",
        notes: str = "",
        description: str = "",
        details: list[dict] = None,
        weekly_shift_template_details: list[WeeklyShiftTemplateDetail] = None,
    ) -> WeeklyShiftTemplate:
        """
        Create a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
        """
        # check for permissions for add weekly shift template
        if not self.permission_service.check_for_permission("add_weeklyshifttemplate"):
            raise PermissionDenied()

        if details:
            # Validate details
            self._validate_details_fields(details)

        # Create WeeklyShiftTemplate
        template = WeeklyShiftTemplate.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
            description=description,
        )

        # Create WeeklyShiftTemplateDetails
        if details:
            self.weeklyshifttemplatedetailservice.create_bulk(details=details)

            # Check for overlapping details
            self._check_no_overlapping_details(template)

        if weekly_shift_template_details:
            template.weekly_shift_template_details.set(weekly_shift_template_details)

        template.full_clean()
        template.save(user=self.user)

        return template

    @transaction.atomic
    def update(
        self,
        instance: WeeklyShiftTemplate,
        data: dict,
    ) -> WeeklyShiftTemplate:
        """
        Update a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
        """
        # check for permissions for change weekly shift template
        if not self.permission_service.check_for_permission(
            "change_weeklyshifttemplate"
        ):
            raise PermissionDenied()

        fields = [
            "name",
            "external_id",
            "notes",
            "description",
            "weekly_shift_template_details",
        ]

        template, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

        details = data.get("details", [])

        if details:
            # Validate details
            self._validate_details_fields(details)

            # Process details
            self._process_details(template, details)

            # Check for overlapping details
            self._check_no_overlapping_details(template)

        template.full_clean()
        template.save(user=self.user)

        return template

    @transaction.atomic
    def delete(self, template: WeeklyShiftTemplate) -> None:
        """
        Delete a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
        """
        # check for permissions for delete weekly shift template
        if not self.permission_service.check_for_permission(
            "delete_weeklyshifttemplate"
        ):
            raise PermissionDenied()

        template.delete()
        return True


# -----------------------------------------------------------------------------
# OperationalExceptionTypeService
# -----------------------------------------------------------------------------


class OperationalExceptionTypeService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self, name: str, external_id: str = "", notes: str = ""
    ) -> OperationalExceptionType:
        # check for permissions for add operational exception type
        if not self.permission_service.check_for_permission(
            "add_operationalexceptiontype"
        ):
            raise PermissionDenied()

        exception_type = OperationalExceptionType.objects.create(
            name=name, external_id=external_id, notes=notes
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
