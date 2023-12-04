from django.db.models.query import QuerySet

from .models import WeeklyShiftTemplateDetail


def weekly_shift_template_detail_list_overlapping(
    current_detail: WeeklyShiftTemplateDetail
) -> QuerySet[WeeklyShiftTemplateDetail]:
    """
    Retrieve overlapping WeeklyShiftTemplateDetails for a given shift detail.

    Overlapping is defined as any shift that has a start time before the end time
    of the current shift and an end time after the start time of the current shift.
    """
    overlapping_details = WeeklyShiftTemplateDetail.objects.filter(
        weekly_shift_template=current_detail.weekly_shift_template,
        day_of_week=current_detail.day_of_week,
        start_time__lt=current_detail.end_time,
        end_time__gt=current_detail.start_time,
    )

    if current_detail.id:
        overlapping_details = overlapping_details.exclude(id=current_detail.id)

    return overlapping_details
