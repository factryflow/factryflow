from django.urls import path

from .views import (
    RESOURCE_VIEWS,
    RESOURCE_GROUP_VIEWS,
)

urlpatterns = [
    # resources urls
    path("resource/new/", RESOURCE_VIEWS.show_model_form, name="resource_form"),
    path(
        "resource-create/",
        RESOURCE_VIEWS.create_or_update_model_instance,
        name="resource_create",
    ),
    path("resources/", RESOURCE_VIEWS.get_all_instances, name="resources"),
    path(
        "resource/delete/<int:id>/",
        RESOURCE_VIEWS.delete_obj_instance,
        name="delete_resource",
    ),
    path(
        "resource/view/<int:id>/", RESOURCE_VIEWS.show_model_form, name="view_resource"
    ),
    path(
        "resource/view/<int:id>/edit=<str:edit>",
        RESOURCE_VIEWS.show_model_form,
        name="edit_resource",
    ),
    path(
        "resource/view/<int:id>/field=<str:field>",
        RESOURCE_VIEWS.show_model_form,
        name="resource_dependencies",
    ),
    # resource groups urls
    path(
        "resource-group/new/",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="resource_group_form",
    ),
    path(
        "resource-group-create/",
        RESOURCE_GROUP_VIEWS.create_or_update_model_instance,
        name="resource_group_create",
    ),
    path(
        "resource-groups/",
        RESOURCE_GROUP_VIEWS.get_all_instances,
        name="resource_groups",
    ),
    path(
        "resource-group/delete/<int:id>/",
        RESOURCE_GROUP_VIEWS.delete_obj_instance,
        name="delete_resource_group",
    ),
    path(
        "resource-group/view/<int:id>/",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="view_resource_group",
    ),
    path(
        "resource-group/view/<int:id>/edit=<str:edit>",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="edit_resource_group",
    ),
    path(
        "resource-groups/view/<int:id>/field=<str:field>",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="resource_group_dependencies",
    ),
]
