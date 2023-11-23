from datetime import strptime

from common.utils.service_helpers import create_or_update_model
from django.core.exceptions import ValidationError
from django.db import transaction
from resource_manager.models import Resource

from .models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)


def parse_time(time_str: str):
    """
    Parse a time string (expected in %H:%M format) and return a time object.
    """
    try:
        return strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValidationError(
            f"Invalid time format: '{time_str}'. Expected format HH:MM."
        )


def validate_no_overlap(details: list[dict]):
    """
    Validate that there are no overlapping time intervals for the same weekday.
    The details are first sorted by day_of_week and start_time for efficient comparison.
    Only hours and minutes are considered for each time interval.
    """
    for detail in details:
        detail["start_time"] = parse_time(detail["start_time"])
        detail["end_time"] = parse_time(detail["end_time"])

    # Sort details by day_of_week and start_time
    sorted_details = sorted(details, key=lambda x: (x["day_of_week"], x["start_time"]))

    # Check for overlaps
    for current_detail, next_detail in zip(sorted_details, sorted_details[1:]):
        if (
            current_detail["day_of_week"] == next_detail["day_of_week"]
            and current_detail["end_time"] > next_detail["start_time"]
        ):
            raise ValidationError(
                f"Overlapping times detected: Day {current_detail['day_of_week']} between "
                f"{current_detail['end_time'].strftime('%H:%M')} and {next_detail['start_time'].strftime('%H:%M')}."
            )


@transaction.atomic
def create_update_weekly_shift_template(
    template_data: dict,
    template_details_data: list[dict] = [],
) -> WeeklyShiftTemplate:
    """
    Create or update a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
    """

    validate_no_overlap(template_details_data)

    template = create_or_update_model(WeeklyShiftTemplate, template_data)

    # Validate and save WeeklyShiftTemplate
    template.full_clean()
    template.save()

    # Create or update WeeklyShiftTemplateDetails
    for detail_data in template_details_data:
        detail = create_or_update_model(
            WeeklyShiftTemplateDetail,
            detail_data,
        )

        # Validate and save WeeklyShiftTemplateDetail
        detail.full_clean()
        detail.save()

    return template


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

    exception = create_or_update_model(OperationalException, exception_data)

    # Set the related objects
    exception.operational_exception_type = exception_type
    exception.weekly_shift_template = weekly_shift_template
    exception.resource = resource

    exception.full_clean()
    exception.save()

    return exception
