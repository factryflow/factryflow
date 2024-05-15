from django.db import models

from common.models import BaseModelWithExtras
from simple_history.models import HistoricalRecords


class Item(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    history = HistoricalRecords(table_name="item_history")

    class Meta:
        db_table = "item"

    def __str__(self):
        return self.name
