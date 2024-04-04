from django.db import models

from common.models import BaseModelWithExtras


class Item(BaseModelWithExtras):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "item"

    def __str__(self):
        return self.name