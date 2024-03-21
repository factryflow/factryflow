from django.urls import path

from .views import WEEKLY_SHIFT_TEMPLATE_VIEWS, WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS, OPERATIONAL_EXCEPTION_TYPE_VIEWS, OPERATIONAL_EXCEPTION_VIEWS

urlpatterns = [
    # weekly shift template urls
    path(
        "weekly_shift_templates/new/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="weekly_shift_template_form",
    ),
    path(
        "weekly_shift_template-create/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.create_or_update_model_instance,
        name="weekly_shift_template_create",
    ),
    path(
        "weekly_shift_templates/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.get_all_instances,
        name="weekly_shift_template",
    ),
    path(
        "weekly_shift_templates/delete/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.delete_obj_instance,
        name="delete_weekly_shift_template",
    ),
    path(
        "weekly_shift_templates/view/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="view_weekly_shift_template",
    ),
    path(
        "weekly_shift_templates/view/<int:id>/edit=<str:edit>",
        WEEKLY_SHIFT_TEMPLATE_VIEWS.show_model_form,
        name="edit_weekly_shift_template",
    ),
    
    # weekly shift template detail urls
    path(
        "weekly_shift_template_details/new/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.show_model_form,
        name="weekly_shift_template_detail_form",
    ),
    path(
        "weekly_shift_template_detail-create/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.create_or_update_model_instance,
        name="weekly_shift_template_detail_create",
    ),
    path(
        "weekly_shift_template_details/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.get_all_instances,
        name="weekly_shift_template_detail",
    ),
    path(
        "weekly_shift_template_details/delete/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.delete_obj_instance,
        name="delete_weekly_shift_template_detail",
    ),
    path(
        "weekly_shift_template_details/view/<int:id>/",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.show_model_form,
        name="view_weekly_shift_template_detail",
    ),
    path(
        "weekly_shift_template_details/view/<int:id>/edit=<str:edit>",
        WEEKLY_SHIFT_TEMPLATE_DETAIL_VIEWS.show_model_form,
        name="edit_weekly_shift_template_detail",
    ),

    # operational exception type urls
    path(
        "operational_exception_types/new/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.show_model_form,
        name="operational_exception_type_form",
    ),
    path(
        "operational_exception_type-create/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.create_or_update_model_instance,
        name="operational_exception_type_create",
    ),
    path(
        "operational-exception-types/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.get_all_instances,
        name="operational_exception_type",
    ),
    path(
        "operational_exception_types/delete/<int:id>/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.delete_obj_instance,
        name="delete_operational_exception_type",
    ),
    path(
        "operational_exception_types/view/<int:id>/",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.show_model_form,
        name="view_operational_exception_type",
    ),
    path(
        "operational_exception_types/view/<int:id>/edit=<str:edit>",
        OPERATIONAL_EXCEPTION_TYPE_VIEWS.show_model_form,
        name="edit_operational_exception_type",
    ),


    # operational exception urls
    path(
        "operational_exceptions/new/",
        OPERATIONAL_EXCEPTION_VIEWS.show_model_form,
        name="operational_exception_form",
    ),
    path(
        "operational_exception-create/",
        OPERATIONAL_EXCEPTION_VIEWS.create_or_update_model_instance,
        name="operational_exception_create",
    ),
    path(
        "operational_exceptions/",
        OPERATIONAL_EXCEPTION_VIEWS.get_all_instances,
        name="operational_exception",
    ),
    path(
        "operational_exceptions/delete/<int:id>/",
        OPERATIONAL_EXCEPTION_VIEWS.delete_obj_instance,
        name="delete_operational_exception",
    ),
    path(
        "operational_exceptions/view/<int:id>/",
        OPERATIONAL_EXCEPTION_VIEWS.show_model_form,
        name="view_operational_exception",
    ),
    path(
        "operational_exceptions/view/<int:id>/edit=<str:edit>",
        OPERATIONAL_EXCEPTION_VIEWS.show_model_form,
        name="edit_operational_exception",
    ),
]
