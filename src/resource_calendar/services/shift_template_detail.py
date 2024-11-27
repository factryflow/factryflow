from datetime import datetime, time

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from resource_calendar.models import (
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
        weekly_shift_template: WeeklyShiftTemplate,
        day_of_week: int,
        start_time: str | time,
        end_time: str | time,
        custom_fields: dict = None,
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
            weekly_shift_template=weekly_shift_template,
            day_of_week=day_of_week,
            start_time=self._parse_time(start_time),
            end_time=self._parse_time(end_time),
            custom_fields=custom_fields,
        )

        weekly_shift_template_detail.full_clean()
        weekly_shift_template_detail.save(user=self.user)

        return weekly_shift_template_detail

    @transaction.atomic
    def create_bulk(
        self,
        template: WeeklyShiftTemplate,
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

        list_of_details = []

        for detail_data in details:
            detail = self.create(
                weekly_shift_template=template,
                day_of_week=detail_data["day_of_week"],
                start_time=detail_data["start_time"],
                end_time=detail_data["end_time"],
            )
            list_of_details.append(detail)

        return list_of_details

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
            "weekly_shift_template",
            "day_of_week",
            "start_time",
            "end_time",
            "custom_fields",
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
