# import time
from datetime import datetime, time

import numpy as np
from factryengine import Resource as SchedulerResource
from resource_calendar.models import WeeklyShiftTemplate
from resource_manager.models import Resource

from .constants import DAY_IN_MINUTES, WEEK_IN_MINUTES


class SchedulingService:
    def __init__(self, plan_start_date: datetime, horizon_weeks: int):
        self.plan_start_date = plan_start_date
        self.plan_start_weekday = plan_start_date.weekday()
        self.plan_start_minutes = self.plan_start_weekday * DAY_IN_MINUTES
        self.horizon_weeks = horizon_weeks
        self.horizon_minutes = horizon_weeks * WEEK_IN_MINUTES
        self.weekly_shift_templates_windows_dict = (
            self._get_weekly_shift_template_windows_dict()
        )

    def run(self):
        # create resources
        resources = Resource.objects.all()
        scheduler_resources = []
        for resource in resources:
            available_windows = self.weekly_shift_templates_windows_dict.get(
                resource.weekly_shift_template_id, []
            )
            scheduler_resource = SchedulerResource(
                id=resource.id, available_windows=available_windows
            )
            scheduler_resources.append(scheduler_resource)
        # create tasks
        pass

    def _get_weekly_shift_template_windows_dict(self) -> dict:
        weekly_shift_templates = WeeklyShiftTemplate.objects.all()
        weekly_shift_template_windows_dict = {}
        for weekly_shift_template in weekly_shift_templates:
            weekly_shift_template_windows_dict[
                weekly_shift_template.id
            ] = self._weekly_shift_template_to_windows(weekly_shift_template)
        return weekly_shift_template_windows_dict

    def _weekly_shift_template_to_windows(
        self, weekly_shift_template: WeeklyShiftTemplate
    ):
        details = weekly_shift_template.details.all()

        weekly_windows = [self._detail_to_minutes(detail) for detail in details]
        windows = self._calculate_windows(weekly_windows)

        return windows

    def _calculate_windows(self, weekly_windows: list):
        weekly_windows = np.array(weekly_windows)
        # Create an increment array
        increment = WEEK_IN_MINUTES * np.arange(self.horizon_weeks + 1).reshape(
            -1, 1, 1
        )

        # Repeat the pattern and add the increment
        windows = weekly_windows + increment

        # subtract plan start
        windows = windows - self.plan_start_minutes

        # filter
        windows = windows[(windows >= 0) & (windows <= self.horizon_minutes)]

        return windows.reshape(-1, 2)

    def _detail_to_minutes(self, detail):
        start_time_minutes = self._time_to_minutes(detail.start_time)
        end_time_minutes = self._time_to_minutes(detail.end_time)
        week_offset_minutes = detail.day_of_week * DAY_IN_MINUTES
        return (
            start_time_minutes + week_offset_minutes,
            end_time_minutes + week_offset_minutes,
        )

    def _time_to_minutes(self, time: time):
        return time.hour * 60 + time.minute
