from common.utils.views import add_notification_headers
from common.views import CRUDView, CustomTableView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from job_manager.models import JobStatusChoices, Task, TaskStatusChoices

# Create your views here.
from .forms import (
    AssigmentRuleCriteriaForm,
    AssigmentRuleForm,
    AssignmentConstraintForm,
    TaskResourceAssigmentForm,
)
from .models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    TaskResourceAssigment,
    TaskRuleAssignment,
    Operator,
)
from .services import (
    AssigmentRuleCriteriaService,
    AssigmentRuleService,
    AssignmentConstraintService,
    TaskResourceAssigmentService,
)

from job_manager.models import Task, TaskStatusChoices, JobStatusChoices
from .utils import get_matching_assignment_rules_with_tasks, get_model_fields

# ------------------------------------------------------------------------------
# Task Resource Assignement Views
# ------------------------------------------------------------------------------

TASK_RESOURCE_ASSIGNMENT_MODEL_FIELDS = [
    "id",
    "task",
    "assigment_rule",
]

TASK_RESOURCE_ASSIGNMENT_TABLE_HEADERS = [
    "ID",
    "Task",
    "Assigment Rule",
]

TASK_RESOURCE_ASSIGNMENT_SEARCH_FIELDS = ["task", "assigment_rule"]

TASK_RESOURCE_ASSIGNMENT_TABLE_VIEW = CustomTableView(
    model=TaskResourceAssigment,
    model_name="task_resource_assigment",
    fields=TASK_RESOURCE_ASSIGNMENT_MODEL_FIELDS,
    headers=TASK_RESOURCE_ASSIGNMENT_TABLE_HEADERS,
    search_fields_list=TASK_RESOURCE_ASSIGNMENT_SEARCH_FIELDS,
)

TASK_RESOURCE_ASSIGNMENT_VIEWS = CRUDView(
    model=TaskResourceAssigment,
    model_name="task_resource_assigments",
    model_service=TaskResourceAssigmentService,
    model_form=TaskResourceAssigmentForm,
    model_table_view=TASK_RESOURCE_ASSIGNMENT_TABLE_VIEW,
)

# ------------------------------------------------------------------------------
# AssigmentRule Views
# ------------------------------------------------------------------------------

ASSIGMENT_RULE_MODEL_FIELDS = [
    "id",
    "order",
    "name",
    "notes",
    "description",
    "work_center",
    "is_active",
]
ASSIGMENT_RULE_TABLE_HEADERS = [
    "ID",
    "Priority",
    "Name",
    "Notes",
    "Description",
    "Work Center",
    "Is Active",
]

ASSIGMENT_RULE_SEARCH_FIELDS = ["name", "description", "external_id"]

ASSIGMENT_RULE_MODEL_RELATION_HEADERS = [
    "RULE CRITERIA",
    "TASK",
    "HISTORY",
]

ASSIGMENT_RULE_MODEL_RELATION_FIELDS = {
    "rule_criteria": {
        "model": AssigmentRuleCriteria,
        "model_name": "assigment_rule_criteria",
        "related_name": "assigment_rule",
        "headers": ["ID", "field", "operator", "value"],
        "fields": ["id", "field", "operator", "value"],
        "select_fields": {
            "field": get_model_fields(
                "Task", "job_manager", ["item", "task_type", "job", "work_center"]
            ),
            "operator": Operator.choices,
        },
        "relationship_fields": "assigment_rule",
        "show_edit_actions": True,
    },
    "task": {
        "model": TaskRuleAssignment,
        "model_name": "task_rule_assignment",
        "related_name": "assigment_rule",
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

ASSIGMENT_RULE_CRITERIA_FORMSET_FORM_FIELDS = ["field", "operator", "value"]

ASSIGMENT_RULE_CRITERIA_FORMSET_OPTIONS = [
    AssigmentRuleCriteria,
    AssigmentRuleCriteriaForm,
    "criteria",
    ASSIGMENT_RULE_CRITERIA_FORMSET_FORM_FIELDS,
    "assigment_rule_criteria",
]

ASSIGMENT_RULE_TABLE_VIEW = CustomTableView(
    model=AssigmentRule,
    model_name="assigment_rule",
    fields=ASSIGMENT_RULE_MODEL_FIELDS,
    headers=ASSIGMENT_RULE_TABLE_HEADERS,
    model_relation_headers=ASSIGMENT_RULE_MODEL_RELATION_HEADERS,
    model_relation_fields=ASSIGMENT_RULE_MODEL_RELATION_FIELDS,
    search_fields_list=ASSIGMENT_RULE_SEARCH_FIELDS,
    order_by_field="order",
)

ASSIGMENT_RULE_VIEWS = CRUDView(
    model=AssigmentRule,
    model_name="assigment_rules",
    model_service=AssigmentRuleService,
    model_form=AssigmentRuleForm,
    model_table_view=ASSIGMENT_RULE_TABLE_VIEW,
    ordered_model=True,
    formset_options=ASSIGMENT_RULE_CRITERIA_FORMSET_OPTIONS,
)


# ------------------------------------------------------------------------------
# AssigmentRuleCriteria Views
# ------------------------------------------------------------------------------

ASSIGMENT_RULE_CRITERIA_MODEL_FIELDS = [
    "id",
    "assigment_rule",
    "field",
    "operator",
    "value",
]
ASSIGMENT_RULE_CRITERIA_TABLE_HEADERS = [
    "ID",
    "Assigment Rule",
    "Field",
    "Operator",
    "Value",
]

ASSIGMENT_RULE_CRITERIA_SEARCH_FIELDS = ["assigment_rule", "field", "operator", "value"]

ASSIGNMENT_STATUS_FILTER_FIELD = "operator"

ASSIGMENT_RULE_CRITERIA_TABLE_VIEW = CustomTableView(
    model=AssigmentRuleCriteria,
    model_name="assigment_rule_criteria",
    fields=ASSIGMENT_RULE_CRITERIA_MODEL_FIELDS,
    headers=ASSIGMENT_RULE_CRITERIA_TABLE_HEADERS,
    search_fields_list=ASSIGMENT_RULE_CRITERIA_SEARCH_FIELDS,
    status_filter_field=ASSIGNMENT_STATUS_FILTER_FIELD,
)

ASSIGMENT_RULE_CRITERIA_VIEWS = CRUDView(
    model=AssigmentRuleCriteria,
    model_name="assigment_rule_criteria",
    model_service=AssigmentRuleCriteriaService,
    model_form=AssigmentRuleCriteriaForm,
    model_table_view=ASSIGMENT_RULE_CRITERIA_TABLE_VIEW,
    sub_model_relation=True,
)


# ------------------------------------------------------------------------------
# AssignmentConstraint Views
# ------------------------------------------------------------------------------

ASSIGNMENT_CONSTRAINT_MODEL_FIELDS = [
    "id",
    "task",
    "assignment_rule",
    "resource_group",
    "resources",
    "resource_count",
    "use_all_resources",
]

ASSIGNMENT_CONSTRAINT_TABLE_HEADERS = [
    "ID",
    "Task",
    "Assignment Rule",
    "Resource Group",
    "Resources",
    "Resource Count",
    "Use All Resources",
]

ASSIGNMENT_CONSTRAINT_SEARCH_FIELDS = [
    "task",
    "assignment_rule",
    "resource_group",
    "resources",
    "resource_count",
    "use_all_resources",
]

ASSIGNMENT_CONSTRAINT_MODEL_RELATION_HEADERS = [
    "Resources",
    "History",
]

ASSIGNMENT_CONSTRAINT_MODEL_RELATION_FIELDS = {
    "resources": {
        "model_name": "resources",
        "related_name": "resources",
        "headers": ["ID", "Resource Name"],
        "fields": ["id", "name"],
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


ASSIGNMENT_CONSTRAINT_TABLE_VIEW = CustomTableView(
    model=AssignmentConstraint,
    model_name="assignment_constraint",
    fields=ASSIGNMENT_CONSTRAINT_MODEL_FIELDS,
    headers=ASSIGNMENT_CONSTRAINT_TABLE_HEADERS,
    search_fields_list=ASSIGNMENT_CONSTRAINT_SEARCH_FIELDS,
    model_relation_headers=ASSIGNMENT_CONSTRAINT_MODEL_RELATION_HEADERS,
    model_relation_fields=ASSIGNMENT_CONSTRAINT_MODEL_RELATION_FIELDS,
)

ASSIGNMENT_CONSTRAINT_VIEWS = CRUDView(
    model=AssignmentConstraint,
    model_name="assignment_constraints",
    model_service=AssignmentConstraintService,
    model_form=AssignmentConstraintForm,
    model_table_view=ASSIGNMENT_CONSTRAINT_TABLE_VIEW,
)

# ------------------------------------------------------------------------------
# Matching Rule API
# ------------------------------------------------------------------------------


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
        )

        if tasks.count() == 0:
            raise Exception("Tasks not found!")

        result = get_matching_assignment_rules_with_tasks(tasks)

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


# ------------------------------------------------------------------------------
# Ordered Model APIs to manage the order of the rules based on the work center
# ------------------------------------------------------------------------------


def change_assignment_rule_priority(request, id: int, direction: str):
    """
    Move the rule up or down in the order.

    Parameters:
    -----------
        id: int - The id of the rule.
        direction: str - The direction to move the rule. It can be either "up" or "down".

    Returns:
    --------
        dict: A dictionary containing the message of the operation.
    """
    max_order_count = AssigmentRule.objects.count() - 1

    response = HttpResponse(status=302)
    response["Location"] = reverse("assigment_rules")

    if direction not in ["up", "down"]:
        response = HttpResponse(status=400)
        message = "Invalid direction. Use 'up' or 'down'."
        add_notification_headers(response, message, "error")
        return response

    try:
        rule = AssigmentRule.objects.get(id=id)

        if direction == "up" and rule.order > 0:
            rule.up()

        elif direction == "down" and rule.order < max_order_count:
            rule.down()

        if request.htmx:
            response = render(
                request,
                "objects/list.html#all-assigment_rules-table",
                {"rows": AssigmentRule.objects.all().order_by("order")},
            )
            return response

        return response

    except AssigmentRule.DoesNotExist:
        response = HttpResponse(status=404)
        message = "Rule not found."
        add_notification_headers(response, message, "error")
        return response

    except Exception as e:
        message = f"An error occurred: {str(e)}"
        add_notification_headers(response, message, "error")
        return response
