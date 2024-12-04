from common.models import Operator
from common.utils.views import get_model_fields
from common.utils.views import add_notification_headers
from common.views import CRUDView, CustomTableView
from django.http import HttpResponse

# Create your views here.
from job_manager.models.job import JobStatusChoices
from job_manager.models.task import Task, TaskStatusChoices

from microbatching.forms.microbatch_rule import (
    MicrobatchRuleCriteriaForm,
    MicrobatchRuleForm,
)
from microbatching.models.microbatch_rule import (
    MicrobatchRule,
    MicrobatchRuleCriteria,
    MicrobatchRuleTaskMatch,
)
from microbatching.services.microbatch_rule import (
    MicrobatchRuleCriteriaService,
    MicrobatchRuleService,
)
from microbatching.utils.microbatch_rule import create_microbatch_rule_matches

# ------------------------------------------------------------------------------
# Microbatch Views
# ------------------------------------------------------------------------------

MICROBATCH_RULE_MODEL_FIELDS = [
    "id",
    "name",
]

MICROBATCH_RULE_SEARCH_FIELDS = [
    "id",
    "name",
]

MICROBATCH_RULE_MODEL_RELATION_HEADERS = [
    "RULE CRITERIA",
    "MATCHING_TASKS",
    "HISTORY",
]

MICROBATCH_RULE_MODEL_RELATION_FIELDS = {
    "rule_criteria": {
        "model": MicrobatchRuleCriteria,
        "model_name": "microbatch_rule_criteria",
        "related_name": "microbatch_rule",
        "headers": ["ID", "field", "operator", "value"],
        "fields": ["id", "field", "operator", "value"],
        "show_edit_actions": False,
    },
    "matching_tasks": {
        "model": MicrobatchRuleTaskMatch,
        "model_name": "microbatch_rule_task_match",
        "related_name": "microbatch_rule",
        "headers": ["ID", "Task", "Rule Applied"],
        "fields": ["id", "task", "is_applied"],
        "show_edit_actions": False,
    },
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "History Date", "History Type", "History User"],
        "fields": ["history_id", "history_date", "history_type", "history_user"],
        "show_edit_actions": False,
    },
}

MICROBATCH_RULE_CRITERIA_FORMSET_FORM_FIELDS = ["field", "operator", "value"]

MICROBATCH_RULE_CRITERIA_FORMSET_OPTIONS = [
    MicrobatchRuleCriteria,
    MicrobatchRuleCriteriaForm,
    "criteria",
    MICROBATCH_RULE_CRITERIA_FORMSET_FORM_FIELDS,
    "microbatch_rule_criteria",
]

MICROBATCH_RULE_TABLE_VIEW = CustomTableView(
    model=MicrobatchRule,
    model_name="microbatch_rule",
    fields=MICROBATCH_RULE_MODEL_FIELDS,
    model_relation_headers=MICROBATCH_RULE_MODEL_RELATION_HEADERS,
    model_relation_fields=MICROBATCH_RULE_MODEL_RELATION_FIELDS,
    search_fields_list=MICROBATCH_RULE_SEARCH_FIELDS,
)

MICROBATCH_RULE_VIEWS = CRUDView(
    model=MicrobatchRule,
    model_name="microbatch_rules",
    model_service=MicrobatchRuleService,
    model_form=MicrobatchRuleForm,
    model_table_view=MICROBATCH_RULE_TABLE_VIEW,
    formset_options=MICROBATCH_RULE_CRITERIA_FORMSET_OPTIONS,
    list_template_name="microbatching/microbatch_rule/list.html",
)

# ------------------------------------------------------------------------------
# MicrobatchtRuleCriteria Views
# ------------------------------------------------------------------------------

MICROBATCH_RULE_CRITERIA_MODEL_FIELDS = [
    "id",
    "microbatch_rule",
    "field",
    "operator",
    "value",
]

MICROBATCH_RULE_CRITERIA_SEARCH_FIELDS = [
    "id",
    "microbatch_rule",
    "field",
    "operator",
    "value",
]


MICROBATCH_RULE_CRITERIA_TABLE_VIEW = CustomTableView(
    model=MicrobatchRuleCriteria,
    model_name="microbatch_rule_criteria",
    fields=MICROBATCH_RULE_CRITERIA_MODEL_FIELDS,
    search_fields_list=MICROBATCH_RULE_CRITERIA_SEARCH_FIELDS,
)

MICROBATCH_RULE_CRITERIA_VIEWS = CRUDView(
    model=MicrobatchRuleCriteria,
    model_name="microbatch_rule_criteria",
    model_service=MicrobatchRuleCriteriaService,
    model_form=MicrobatchRuleCriteriaForm,
    model_table_view=MICROBATCH_RULE_CRITERIA_TABLE_VIEW,
    sub_model_relation=True,
)


def match_rules_with_tasks(request):
    """
    Match rules with tasks.
    """
    try:
        tasks = Task.objects.filter(
            task_status=TaskStatusChoices.NOT_STARTED,
            job__job_status__in=[
                JobStatusChoices.IN_PROGRESS,
                JobStatusChoices.NOT_PLANNED,
            ],
            parent=None,
        )

        if tasks.count() == 0:
            raise Exception("Tasks not found!")

        result = create_microbatch_rule_matches(tasks)

        response = HttpResponse(status=204)
        add_notification_headers(
            response,
            result["message"],
            result["status"],
        )

        return response
    except Exception as e:
        response = HttpResponse(status=500)
        add_notification_headers(
            response,
            str(e),
            "error",
        )
        return response
