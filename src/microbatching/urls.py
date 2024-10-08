from django.urls import path

from microbatching.views.microbatch_rule import (
    MICROBATCH_RULE_VIEWS,
)

urlpatterns = [
    # assigment_rule urls
    path(
        "microbatch-rules/new/",
        MICROBATCH_RULE_VIEWS.show_model_form,
        name="microbatch_rules_form",
    ),
    path(
        "microbatch-rules/new/<int:formset_count>",
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
]
