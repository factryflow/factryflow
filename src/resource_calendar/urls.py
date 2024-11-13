from django.urls import path

from .views import (
    WEEKLY_SHIFT_TEMPLATE_VIEWS,
    WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS,
    OPERATIONAL_EXCEPTION_TYPE_VIEWS,
    OPERATIONAL_EXCEPTION_VIEWS,
)

urlpatterns = [
    # weekly shift template urls
    path(
        "weekly-shift-templates/new/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="weekly_shift_templates_form",
    ),
    path(
        "weekly-shift-templates/new/formset-count=<int:formset_count>",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="weekly_shift_templates_formset",
    ),
    path(
        "weekly-shift-templates-create/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.create_or_update_model_instance,
        name="weekly_shift_templates_create",
    ),
    path(
        "weekly-shift-templates/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.get_all_instances,
        name="weekly_shift_templates",
    ),
    path(
        "weekly-shift-templates/delete/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.delete_obj_instance,
        name="delete_weekly_shift_templates",
    ),
    path(
        "weekly-shift-templates/view/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="view_weekly_shift_templates",
    ),
    path(
        "weekly-shift-templates/view/<int:id>/edit=<str:edit>",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="edit_weekly_shift_templates",
    ),
    path(
        "weekly-shift-templates/view/<int:id>/field=<str:field>",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="weekly_shift_templates_relationships",
    ),
    # weekly shift template detail urls
    path(
        "weekly-shift-template-details/new/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.show_model_form,
        name="weekly_shift_template_detail_form",
    ),
    path(
        "weekly-shift-template-details-create/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.create_or_update_model_instance,
        name="weekly_shift_template_detail_create",
    ),
    path(
        "weekly-shift-template-details/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.get_all_instances,
        name="weekly_shift_template_detail",
    ),
    path(
        "weekly-shift-template-details/delete/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.delete_obj_instance,
        name="delete_weekly_shift_template_detail",
    ),
    path(
        "weekly-shift-template-details/view/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.show_model_form,
        name="view_weekly_shift_template_detail",
    ),
    path(
        "weekly-shift-template-details/view/<int:id>/edit=<str:edit>",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.show_model_form,
        name="edit_weekly_shift_template_detail",
    ),
    path(
        "weekly-shift-template-details/view/<int:id>/field=<str:field>",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.show_model_form,
        name="weekly_shift_template_detail_relationships",
    ),
    # operational exception type urls
    path(
        "operational-exception-types/new/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.show_model_form,
        name="operational_exception_types_form",
    ),
    path(
        "operational-exception-types-create/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.create_or_update_model_instance,
        name="operational_exception_types_create",
    ),
    path(
        "operational-exception-types/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.get_all_instances,
        name="operational_exception_types",
    ),
    path(
        "operational-exception-types/delete/<int:id>/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.delete_obj_instance,
        name="delete_operational_exception_types",
    ),
    path(
        "operational-exception-types/view/<int:id>/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.show_model_form,
        name="view_operational_exception_types",
    ),
    path(
        "operational-exception-types/view/<int:id>/edit=<str:edit>",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.show_model_form,
        name="edit_operational_exception_types",
    ),
    path(
        "operational-exception-types/view/<int:id>/field=<str:field>",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.show_model_form,
        name="operational_exception_types_relationships",
    ),
    # operational exception urls
    path(
        "operational-exceptions/new/",
        OPERATIONAL_EXCEPTION_VIEWS.show_model_form,
        name="operational_exceptions_form",
    ),
    path(
        "operational-exceptions-create/",
        OPERATIONAL_EXCEPTION_VIEWS.create_or_update_model_instance,
        name="operational_exceptions_create",
    ),
    path(
        "operational-exceptions/",
        OPERATIONAL_EXCEPTION_VIEWS.get_all_instances,
        name="operational_exceptions",
    ),
    path(
        "operational-exceptions/delete/<int:id>/",
        OPERATIONAL_EXCEPTION_VIEWS.delete_obj_instance,
        name="delete_operational_exceptions",
    ),
    path(
        "operational-exceptions/view/<int:id>/",
        OPERATIONAL_EXCEPTION_VIEWS.show_model_form,
        name="view_operational_exceptions",
    ),
    path(
        "operational-exceptions/view/<int:id>/edit=<str:edit>",
        OPERATIONAL_EXCEPTION_VIEWS.show_model_form,
        name="edit_operational_exceptions",
    ),
    path(
        "operational-exceptions/view/<int:id>/field=<str:field>",
        OPERATIONAL_EXCEPTION_VIEWS.show_model_form,
        name="operational_exceptions_relationships",
    ),
]
