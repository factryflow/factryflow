from datetime import datetime, time

from common.utils.services import build_or_retrieve_instance
from django.core.exceptions import ValidationError
from django.db import transaction
from resource_manager.models import Resource

from .models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)
from .selectors import weekly_shift_template_detail_list_overlapping


def parse_time(time_input: str | time) -> datetime.time:
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
def create_update_weekly_shift_template_detail(
    *,
    detail_data: dict,
    weekly_shift_template: WeeklyShiftTemplate = None,
) -> WeeklyShiftTemplateDetail:
    """
    Create or update a WeeklyShiftTemplateDetail.
    """
    # Parse time strings into time objects
    detail_data["start_time"] = parse_time(detail_data["start_time"])
    detail_data["end_time"] = parse_time(detail_data["end_time"])

    # Create or update WeeklyShiftTemplateDetail
    detail = build_or_retrieve_instance(WeeklyShiftTemplateDetail, detail_data)

    if weekly_shift_template:
        detail.weekly_shift_template = weekly_shift_template

    # Validate
    detail.full_clean()

    # Check for overlapping times
    overlapping_details = weekly_shift_template_detail_list_overlapping(detail)

    if overlapping_details.exists():
        overlapping_detail = overlapping_details.first()
        raise ValidationError(
            f"Overlapping times detected with detail ID {overlapping_detail.id}: "
            f"{overlapping_detail.start_time.strftime('%H:%M')} - {overlapping_detail.end_time.strftime('%H:%M')}"
        )

    # Save
    detail.save()

    return detail


@transaction.atomic
def create_update_weekly_shift_template(
    template_data: dict,
    template_details_data: list[dict] = [],
) -> WeeklyShiftTemplate:
    """
    Create or update a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
    """

    template = build_or_retrieve_instance(WeeklyShiftTemplate, template_data)

    # Validate and save WeeklyShiftTemplate
    template.full_clean()
    template.save()

    # Create or update WeeklyShiftTemplateDetails
    for detail_data in template_details_data:
        create_update_weekly_shift_template_detail(
            detail_data=detail_data, weekly_shift_template=template
        )

    return template


@transaction.atomic
def create_update_operational_exception_type(
    exception_type_data: dict,
) -> OperationalExceptionType:
    """
    Create or update an OperationalExceptionType instance.
    """

    exception_type = build_or_retrieve_instance(
        OperationalExceptionType, exception_type_data
    )

    # Validate and save
    exception_type.full_clean()
    exception_type.save()

    return exception_type


@transaction.atomic
def create_update_operational_exception(
    *,
    exception_data: dict,
    exception_type: OperationalExceptionType,
    weekly_shift_template: WeeklyShiftTemplate = None,
    resource: Resource,
) -> OperationalException:
    """
    Create or update an OperationalException instance.
    """

    exception = build_or_retrieve_instance(OperationalException, exception_data)

    # Set the related objects
    exception.operational_exception_type = exception_type
    exception.weekly_shift_template = weekly_shift_template
    exception.resource = resource

    exception.full_clean()
    exception.save()

    return exception
