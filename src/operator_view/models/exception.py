from django.db import models
from job_manager.models import Task
from resource_calendar.models import OperationalException


class OperatorViewException(OperationalException):
    # Core fields
    item = models.ForeignKey(
        Task,
        on_delete=models.DO_NOTHING,
        related_name="task_item",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.DO_NOTHING,
        related_name="task_name",
    )

    class Meta:
        db_table = "operator_view_exception"
