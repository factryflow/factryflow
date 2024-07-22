from django.urls import path

from .views import (
    TASK_RESOURCE_ASSIGNMENT_VIEWS,
    ASSIGMENT_RULE_VIEWS,
    ASSIGMENT_RULE_CRITERIA_VIEWS,
    ASSIGNMENT_CONSTRAINT_VIEWS,
    match_rules_with_tasks,
)

urlpatterns = [
    # task_resource_assigment urls
    path(
        "task-resource-assigment/new/",
        TASK_RESOURCE_ASSIGNMENT_VIEWS.show_model_form,
        name="task_resource_assigment_form",
    ),
    path(
        "task-resource_assigment-create/",
        TASK_RESOURCE_ASSIGNMENT_VIEWS.create_or_update_model_instance,
        name="task_resource_assigment_create",
    ),
    path(
        "task-resource-assigments/",
        TASK_RESOURCE_ASSIGNMENT_VIEWS.get_all_instances,
        name="task_resource_assigments",
    ),
    path(
        "task-resource-assigment/delete/<int:id>/",
        TASK_RESOURCE_ASSIGNMENT_VIEWS.delete_obj_instance,
        name="delete_task_resource_assigment",
    ),
    path(
        "task-resource-assigment/view/<int:id>/",
        TASK_RESOURCE_ASSIGNMENT_VIEWS.show_model_form,
        name="view_task_resource_assigment",
    ),
    path(
        "task-resource-assigment/view/<int:id>/edit=<str:edit>",
        TASK_RESOURCE_ASSIGNMENT_VIEWS.show_model_form,
        name="edit_task_resource_assigment",
    ),
    path(
        "task-resource-assigment/view/<int:id>/field=<str:field>",
        TASK_RESOURCE_ASSIGNMENT_VIEWS.show_model_form,
        name="task_resource_assigment_dependencies",
    ),
    # assigment_rule urls
    path(
        "assigment-rule/new/",
        ASSIGMENT_RULE_VIEWS.show_model_form,
        name="assigment_rule_form",
    ),
    path(
        "assigment-rule/new/<int:formset_count>",
        ASSIGMENT_RULE_VIEWS.show_model_form,
        name="assigment_rule_formset",
    ),
    path(
        "assigment-rule-create/",
        ASSIGMENT_RULE_VIEWS.create_or_update_model_instance,
        name="assigment_rule_create",
    ),
    path(
        "assigment-rules/",
        ASSIGMENT_RULE_VIEWS.get_all_instances,
        name="assigment_rules",
    ),
    path(
        "assigment-rule/delete/<int:id>/",
        ASSIGMENT_RULE_VIEWS.delete_obj_instance,
        name="delete_assigment_rule",
    ),
    path(
        "assigment-rule/view/<int:id>/",
        ASSIGMENT_RULE_VIEWS.show_model_form,
        name="view_assigment_rule",
    ),
    path(
        "assigment-rule/view/<int:id>/edit=<str:edit>",
        ASSIGMENT_RULE_VIEWS.show_model_form,
        name="edit_assigment_rule",
    ),
    path(
        "assigment-rule/view/<int:id>/field=<str:field>",
        ASSIGMENT_RULE_VIEWS.show_model_form,
        name="assigment_rule_relationships",
    ),
    # assigment_rule_criteria urls
    path(
        "assigment-rule-criteria/new/",
        ASSIGMENT_RULE_CRITERIA_VIEWS.show_model_form,
        name="assigment_rule_criteria_form",
    ),
    path(
        "assigment-rule-criteria-create/",
        ASSIGMENT_RULE_CRITERIA_VIEWS.create_or_update_model_instance,
        name="assigment_rule_criteria_create",
    ),
    path(
        "assigment-rule-criteria/",
        ASSIGMENT_RULE_CRITERIA_VIEWS.get_all_instances,
        name="assigment_rule_criterias",
    ),
    path(
        "assigment-rule-criteria/delete/<int:id>/",
        ASSIGMENT_RULE_CRITERIA_VIEWS.delete_obj_instance,
        name="delete_assigment_rule_criteria",
    ),
    path(
        "assigment-rule-criteria/view/<int:id>/",
        ASSIGMENT_RULE_CRITERIA_VIEWS.show_model_form,
        name="view_assigment_rule_criteria",
    ),
    path(
        "assigment-rule-criteria/view/<int:id>/edit=<str:edit>",
        ASSIGMENT_RULE_CRITERIA_VIEWS.show_model_form,
        name="edit_assigment_rule_criteria",
    ),
    # assignment_constraint urls
    path(
        "assignment-constraint/new/",
        ASSIGNMENT_CONSTRAINT_VIEWS.show_model_form,
        name="assignment_constraint_form",
    ),
    path(
        "assignment-constraint-create/",
        ASSIGNMENT_CONSTRAINT_VIEWS.create_or_update_model_instance,
        name="assignment_constraint_create",
    ),
    path(
        "assignment-constraints/",
        ASSIGNMENT_CONSTRAINT_VIEWS.get_all_instances,
        name="assignment_constraints",
    ),
    path(
        "assignment-constraint/delete/<int:id>/",
        ASSIGNMENT_CONSTRAINT_VIEWS.delete_obj_instance,
        name="delete_assignment_constraint",
    ),
    path(
        "assignment-constraint/view/<int:id>/",
        ASSIGNMENT_CONSTRAINT_VIEWS.show_model_form,
        name="view_assignment_constraint",
    ),
    path(
        "assignment-constraint/view/<int:id>/edit=<str:edit>",
        ASSIGNMENT_CONSTRAINT_VIEWS.show_model_form,
        name="edit_assignment_constraint",
    ),
    path(
        "assignment-constraint/view/<int:id>/field=<str:field>",
        ASSIGNMENT_CONSTRAINT_VIEWS.show_model_form,
        name="assignment_constraint_dependencies",
    ),
    # match rules with tasks
    path(
        "match-rules-with-tasks/",
        match_rules_with_tasks,
        name="match_rules_with_tasks",
    ),
]
