from collections import defaultdict

from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from resource_calendar.models import (
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)
from .shift_template_detail import WeeklyShiftTemplateDetailService


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
        existing_details = WeeklyShiftTemplateDetail.objects.filter(
            weekly_shift_template=template
        ).all()

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
        list_of_details = self.weeklyshifttemplatedetailservice.create_bulk(
            template=template, details=details_to_create
        )

        return list_of_details

    def _check_no_overlapping_details(self, template: WeeklyShiftTemplate) -> None:
        details_by_day = defaultdict(list)

        # get details
        details = WeeklyShiftTemplateDetail.objects.filter(
            weekly_shift_template=template
        ).all()

        # Group details by day of the week
        for detail in details:
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
        weekly_shift_template_details: list[dict] = None,
        custom_fields: dict = None,
    ) -> WeeklyShiftTemplate:
        """
        Create a WeeklyShiftTemplate and its related WeeklyShiftTemplateDetails.
        """
        # check for permissions for add weekly shift template
        if not self.permission_service.check_for_permission("add_weeklyshifttemplate"):
            raise PermissionDenied()

        if weekly_shift_template_details:
            # Validate details
            self._validate_details_fields(weekly_shift_template_details)

        # Create WeeklyShiftTemplate
        template = WeeklyShiftTemplate.objects.create(
            name=name,
            external_id=external_id,
            notes=notes,
            description=description,
            custom_fields=custom_fields,
        )

        # Create WeeklyShiftTemplateDetails
        if weekly_shift_template_details:
            self.weeklyshifttemplatedetailservice.create_bulk(
                template=template, details=weekly_shift_template_details
            )
            # Check for overlapping details
            self._check_no_overlapping_details(template)

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
            "custom_fields",
        ]

        template, _ = model_update(
            instance=instance, fields=fields, data=data, user=self.user
        )

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
