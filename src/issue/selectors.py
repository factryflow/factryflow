from django.db.models.query import QuerySet

from .filters import IssueFilter
from .models import Issue


def issue_list(*, filters=None) -> QuerySet[Issue]:
    """
    Get list of Published issues
    """
    filters = filters or {}

    qs = Issue.objects.all()

    return IssueFilter(filters, qs).qs
