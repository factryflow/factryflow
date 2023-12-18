from collections import defaultdict
from datetime import datetime, time

from common.services import model_update
from django.core.exceptions import ValidationError
from django.db import transaction
from resource_manager.models import Resource

from .models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)


class WeeklyShiftTemplateDetailService:
    def __init__(self):
        pass

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
        *,
        day_of_week: int,
        start_time: str | time,
        end_time: str | time,
        weekly_shift_template: WeeklyShiftTemplate,
    ) -> WeeklyShiftTemplateDetail:
        """
        Create a WeeklyShiftTemplateDetail.
        """

        weekly_shift_template_detail = WeeklyShiftTemplateDetail.objects.create(
            day_of_week=day_of_week,
            start_time=self._parse_time(start_time),
            end_time=self._parse_time(end_time),
            weekly_shift_template=weekly_shift_template,
        )

        weekly_shift_template_detail.full_clean()
        weekly_shift_template_detail.save()

        return weekly_shift_template_detail

    @transaction.atomic
    def create_bulk(
        *self,
        weekly_shift_template: WeeklyShiftTemplate,
        details: list[dict],
    ) -> None:
        """
        Create a list of WeeklyShiftTemplateDetails.
        """
        for detail_data in details:
            WeeklyShiftTemplateDetailService().create(
                day_of_week=detail_data["day_of_week"],
                start_time=detail_data["start_time"],
                end_time=detail_data["end_time"],
                weekly_shift_template=weekly_shift_template,
            )

    @transaction.atomic
    def delete(self, instance: WeeklyShiftTemplateDetail) -> None:
        """
        Delete a WeeklyShiftTemplateDetail.
        """
        instance.delete()


class WeeklyShiftTemplateService:
    def __init__(self):
        pass

    def _process_details(
        self, template: WeeklyShiftTemplate, new_details: list[dict]
    ) -> None:
        """
        Process a list of WeeklyShiftTemplateDetails for a given WeeklyShiftTemplate.
        """
        existing_details = template.details.all()

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
            WeeklyShiftTemplateDetailService().delete(detail)

        # Create new details
        WeeklyShiftTemplateDetailService().create_bulk(
            weekly_shift_template=template, details=details_to_create
        )

    def _check_no_overlapping_details(self, template: WeeklyShiftTemplate) -> None:
        details_by_day = defaultdict(list)

        # Group details by day of the week
        for detail in template.details.all():
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
        *,
        name: str,
        details: list[dict],
    ) -> WeeklyShiftTemplate:
        """
        Create a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
        """
        self._validate_details_fields(details)

        # Create WeeklyShiftTemplate
        template = WeeklyShiftTemplate.objects.create(name=name)

        # Create WeeklyShiftTemplateDetails
        WeeklyShiftTemplateDetailService().create_bulk(
            weekly_shift_template=template, details=details
        )

        # Check for overlapping details
        self._check_no_overlapping_details(template)

        template.full_clean()
        template.save()

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

        fields = [
            "name",
        ]

        template, _ = model_update(instance=instance, fields=fields, data=data)

        details = data.get("details", [])

        if details:
            # Validate details
            self._validate_details_fields(details)

            # Process details
            self._process_details(template, details)

            # Check for overlapping details
            self._check_no_overlapping_details(template)

        template.full_clean()
        template.save()

        return template

    @transaction.atomic
    def delete(template: WeeklyShiftTemplate) -> None:
        """
        Delete a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
        """
        template.delete()


class OperationalExceptionTypeService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(name: str) -> OperationalExceptionType:
        exception_type = OperationalExceptionType.objects.create(name=name)
        exception_type.full_clean()
        exception_type.save()

        return exception_type

    @transaction.atomic
    def update(
        exception_type: OperationalExceptionType, data: dict
    ) -> OperationalExceptionType:
        fields = [
            "name",
        ]

        exception_type, _ = model_update(
            instance=exception_type, fields=fields, data=data
        )

        return exception_type

    @transaction.atomic
    def delete(exception_type: OperationalExceptionType) -> None:
        exception_type.delete()


class OperationalExceptionService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(
        *,
        resource: Resource,
        start_datetime: datetime,
        end_datetime: datetime,
        exception_type: OperationalExceptionType,
        weekly_shift_template: WeeklyShiftTemplate = None,
        external_id: str = "",
        notes="",
    ) -> OperationalException:
        exception = OperationalException.objects.create(
            resource=resource,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            operational_exception_type=exception_type,
            weekly_shift_template=weekly_shift_template,
            external_id=external_id,
            notes=notes,
        )

        exception.full_clean()
        exception.save()

        return exception

    @transaction.atomic
    def update(exception: OperationalException, data: dict) -> OperationalException:
        fields = [
            "resource",
            "start_datetime",
            "end_datetime",
            "operational_exception_type",
            "weekly_shift_template",
            "external_id",
            "notes",
        ]

        exception, _ = model_update(instance=exception, fields=fields, data=data)

        return exception

    @transaction.atomic
    def delete(exception: OperationalException) -> None:
        exception.delete()
