import django_filters

from .models import Issue


class IssueFilter(django_filters.FilterSet):
    class Meta:
        model = Issue
        fields = {
            "title": ["icontains"],
            "status": ["icontains"],
            "task": ["icontains"],
            "issue__comments": ["icontains"],
            "created_at": ["exact", "day__gte"],
        }

    @property
    def qs(self):
        parent = super().qs
        issuer = getattr(self.request, "user", None)

        return parent.filter(status=Issue.status.PUBLISHED) | parent.filter(
            created_by=issuer
        )
