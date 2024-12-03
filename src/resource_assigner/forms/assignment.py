from django import forms

from common.forms import get_select_widget, get_multi_select_widget
from job_manager.models import Task
from resource_manager.models import Resource
from resource_assigner.models import TaskResourceAssigment


# ------------------------------------------------------------------------------
# TaskResource Assignment Forms
# ------------------------------------------------------------------------------


class TaskResourceAssigmentForm(forms.ModelForm):
    class Meta:
        model = TaskResourceAssigment
        fields = "__all__"
        exclude = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "custom_fields",
        ]
        labels = {
            "task": "Task",
            "resources": "Resources",
        }
        widgets = {
            "task": get_select_widget(Task),
            "resources": get_multi_select_widget(Resource),
        }
