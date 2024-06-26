from django.urls import path

from .views import CUSTOM_FIELD_VIEWS

urlpatterns = [
    # custom field urls
    path(
        "custom-fields/new/",
        CUSTOM_FIELD_VIEWS.show_model_form,
        name="custom_field_form",
    ),
    path(
        "custom_field-create/",
        CUSTOM_FIELD_VIEWS.create_or_update_model_instance,
        name="custom_field_create",
    ),
    path("custom-fields/", CUSTOM_FIELD_VIEWS.get_all_instances, name="custom_field"),
    path(
        "custom_fields/delete/<int:id>/",
        CUSTOM_FIELD_VIEWS.delete_obj_instance,
        name="delete_custom_field",
    ),
    path(
        "custom-fields/view/<int:id>/",
        CUSTOM_FIELD_VIEWS.show_model_form,
        name="view_custom_field",
    ),
    path(
        "custom-fields/view/<int:id>/edit=<str:edit>",
        CUSTOM_FIELD_VIEWS.show_model_form,
        name="edit_custom_field",
    ),
]
