import re
from django.db import models

from common.models import BaseModelWithExtras
from simple_history.models import HistoricalRecords


class Item(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    name_first = models.CharField(max_length=150, blank=True, null=True)
    name_middle = models.CharField(max_length=150, blank=True, null=True)
    name_last = models.CharField(max_length=150, blank=True, null=True)

    history = HistoricalRecords(table_name="item_history")

    class Meta:
        db_table = "item"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Set item name components if the item name follows a set pattern
        name_pattern = r'^[A-Za-z0-9]{3}-[A-Za-z0-9]{3}-[A-Za-z0-9]{3}$'
        if re.match(name_pattern, self.name):
            names = self.name.split('-')
            self.name_first = names[0]
            self.name_middle = names[1]
            self.name_last = names[2]
        super(Item, self).save(*args, **kwargs)
