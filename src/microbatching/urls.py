from django.urls import path

from microbatching.views.microbatch_flow import (
    MICROBATCH_FLOW_VIEWS,
    match_flows_with_tasks,
    change_microbatch_flow_priority,
)
from microbatching.views.microbatch_rule import (
    MICROBATCH_RULE_CRITERIA_VIEWS,
    MICROBATCH_RULE_VIEWS,
    match_rules_with_tasks,
)

urlpatterns = [
    # MICROBATCH RULE URLs
    path(
        "microbatch-rules/new/",
        MICROBATCH_RULE_VIEWS.show_model_form,
        name="microbatch_rules_form",
    ),
    path(
        "microbatch-rules/new/formset-count=<int:formset_count>",
        MICROBATCH_RULE_VIEWS.show_model_form,
        name="microbatch_rules_formset",
    ),
    path(
        "microbatch-rules-create/",
        MICROBATCH_RULE_VIEWS.create_or_update_model_instance,
        name="microbatch_rules_create",
    ),
    path(
        "microbatch-rules/",
        MICROBATCH_RULE_VIEWS.get_all_instances,
        name="microbatch_rules",
    ),
    path(
        "microbatch-rules/delete/<int:id>/",
        MICROBATCH_RULE_VIEWS.delete_obj_instance,
        name="delete_microbatch_rules",
    ),
    path(
        "microbatch-rules/view/<int:id>/",
        MICROBATCH_RULE_VIEWS.show_model_form,
        name="view_microbatch_rules",
    ),
    path(
        "microbatch-rules/view/<int:id>/edit=<str:edit>",
        MICROBATCH_RULE_VIEWS.show_model_form,
        name="edit_microbatch_rules",
    ),
    path(
        "microbatch-rules/view/<int:id>/field=<str:field>",
        MICROBATCH_RULE_VIEWS.show_model_form,
        name="microbatch_rules_relationships",
    ),
    # MICROBATCH RULE CRITERIA URLs
    path(
        "microbatch-rule-criteria/new/",
        MICROBATCH_RULE_CRITERIA_VIEWS.show_model_form,
        name="microbatch_rule_criteria_form",
    ),
    path(
        "microbatch-rule-criteria-create/",
        MICROBATCH_RULE_CRITERIA_VIEWS.create_or_update_model_instance,
        name="microbatch_rule_criteria_create",
    ),
    path(
        "microbatch-rule-criteria/",
        MICROBATCH_RULE_CRITERIA_VIEWS.get_all_instances,
        name="microbatch_rule_criteria",
    ),
    path(
        "microbatch-rule-criteria/delete/<int:id>/",
        MICROBATCH_RULE_CRITERIA_VIEWS.delete_obj_instance,
        name="delete_microbatch_rule_criteria",
    ),
    path(
        "microbatch-rule-criteria/view/<int:id>/",
        MICROBATCH_RULE_CRITERIA_VIEWS.show_model_form,
        name="view_microbatch_rule_criteria",
    ),
    path(
        "microbatch-rule-criteria/view/<int:id>/edit=<str:edit>",
        MICROBATCH_RULE_CRITERIA_VIEWS.show_model_form,
        name="edit_microbatch_rule_criteria",
    ),
    # MICROBATCH FLOW URLs
    path(
        "microbatch-flows/new/",
        MICROBATCH_FLOW_VIEWS.show_model_form,
        name="microbatch_flows_form",
    ),
    path(
        "microbatch-flows/new/<int:formset_count>",
        MICROBATCH_FLOW_VIEWS.show_model_form,
        name="microbatch_flows_formset",
    ),
    path(
        "microbatch-flows-create/",
        MICROBATCH_FLOW_VIEWS.create_or_update_model_instance,
        name="microbatch_flows_create",
    ),
    path(
        "microbatch-flows/",
        MICROBATCH_FLOW_VIEWS.get_all_instances,
        name="microbatch_flows",
    ),
    path(
        "microbatch-flows/delete/<int:id>/",
        MICROBATCH_FLOW_VIEWS.delete_obj_instance,
        name="delete_microbatch_flows",
    ),
    path(
        "microbatch-flows/view/<int:id>/",
        MICROBATCH_FLOW_VIEWS.show_model_form,
        name="view_microbatch_flows",
    ),
    path(
        "microbatch-flows/view/<int:id>/edit=<str:edit>",
        MICROBATCH_FLOW_VIEWS.show_model_form,
        name="edit_microbatch_flows",
    ),
    path(
        "microbatch-flows/view/<int:id>/field=<str:field>",
        MICROBATCH_FLOW_VIEWS.show_model_form,
        name="microbatch_flows_relationships",
    ),
    # match rules with tasks
    path(
        "microbatch-rules/match-rules-with-tasks/",
        match_rules_with_tasks,
        name="match_microbatch_rules_with_tasks",
    ),
    path(
        "microbatch-flows/generate-task-flows/",
        match_flows_with_tasks,
        name="generate_task_flows",
    ),
    # change assignment rule priority
    path(
        "change-microbatch-flow-priority/<int:id>/direction=<str:direction>",
        change_microbatch_flow_priority,
        name="change_microbatch_flow_priority",
    ),
]
