from django.urls import path

from .views import CUSTOM_FIELD_VIEWS

urlpatterns = [
    # custom field urls
    path(
        "custom-fields/new/",
        CUSTOM_FIELD_VIEWS.show_model_form,
        name="custom_fields_form",
    ),
    path(
        "custom-fields-create/",
        CUSTOM_FIELD_VIEWS.create_or_update_model_instance,
        name="custom_fields_create",
    ),
    path("custom-fields/", CUSTOM_FIELD_VIEWS.get_all_instances, name="custom_fields"),
    path(
        "custom-fields/delete/<int:id>/",
        CUSTOM_FIELD_VIEWS.delete_obj_instance,
        name="delete_custom_fields",
    ),
    path(
        "custom-fields/view/<int:id>/",
        CUSTOM_FIELD_VIEWS.show_model_form,
        name="view_custom_fields",
    ),
    path(
        "custom-fields/view/<int:id>/edit=<str:edit>",
        CUSTOM_FIELD_VIEWS.show_model_form,
        name="edit_custom_fields",
    ),
]
