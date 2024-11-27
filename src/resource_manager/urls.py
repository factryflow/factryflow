from django.urls import path

from resource_manager.views import (
    RESOURCE_VIEWS,
    RESOURCE_GROUP_VIEWS,
)

urlpatterns = [
    # resources urls
    path("resources/new/", RESOURCE_VIEWS.show_model_form, name="resources_form"),
    path(
        "resources-create/",
        RESOURCE_VIEWS.create_or_update_model_instance,
        name="resources_create",
    ),
    path("resources/", RESOURCE_VIEWS.get_all_instances, name="resources"),
    path(
        "resources/delete/<int:id>/",
        RESOURCE_VIEWS.delete_obj_instance,
        name="delete_resources",
    ),
    path(
        "resources/view/<int:id>/",
        RESOURCE_VIEWS.show_model_form,
        name="view_resources",
    ),
    path(
        "resources/view/<int:id>/edit=<str:edit>",
        RESOURCE_VIEWS.show_model_form,
        name="edit_resources",
    ),
    path(
        "resources/view/<int:id>/field=<str:field>",
        RESOURCE_VIEWS.show_model_form,
        name="resources_relationships",
    ),
    # resource groups urls
    path(
        "resource-groups/new/",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="resource_groups_form",
    ),
    path(
        "resource-groups-create/",
        RESOURCE_GROUP_VIEWS.create_or_update_model_instance,
        name="resource_groups_create",
    ),
    path(
        "resource-groups/",
        RESOURCE_GROUP_VIEWS.get_all_instances,
        name="resource_groups",
    ),
    path(
        "resource-groups/delete/<int:id>/",
        RESOURCE_GROUP_VIEWS.delete_obj_instance,
        name="delete_resource_groups",
    ),
    path(
        "resource-groups/view/<int:id>/",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="view_resource_groups",
    ),
    path(
        "resource-groups/view/<int:id>/edit=<str:edit>",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="edit_resource_groups",
    ),
    path(
        "resource-groups/view/<int:id>/field=<str:field>",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="resource_groups_relationships",
    ),
]
