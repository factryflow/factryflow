from django.urls import path

from .views import (
    RESOURCE_VIEWS,
    RESOURCE_GROUP_VIEWS,
)

urlpatterns = [
    # resources urls
    path("resources/new/", RESOURCE_VIEWS.show_model_form, name="resource_form"),
    path(
        "resource-create/",
        RESOURCE_VIEWS.create_or_update_model_instance,
        name="resource_create",
    ),
    path("resources/", RESOURCE_VIEWS.get_all_instances, name="resource"),
    path(
        "resources/delete/<int:id>/",
        RESOURCE_VIEWS.delete_obj_instance,
        name="delete_resource",
    ),
    path(
        "resources/view/<int:id>/", RESOURCE_VIEWS.show_model_form, name="view_resource"
    ),
    path(
        "resources/view/<int:id>/edit=<str:edit>",
        RESOURCE_VIEWS.show_model_form,
        name="edit_resource",
    ),
    path(
        "resources/view/<int:id>/field=<str:field>",
        RESOURCE_VIEWS.show_model_form,
        name="resource_dependencies",
    ),
    # resource pool urls
    path(
        "resource_pools/new/",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="resource_pool_form",
    ),
    path(
        "resource_pool-create/",
        RESOURCE_GROUP_VIEWS.create_or_update_model_instance,
        name="resource_pool_create",
    ),
    path(
        "resource-pools/", RESOURCE_GROUP_VIEWS.get_all_instances, name="resource_pool"
    ),
    path(
        "resource_pools/delete/<int:id>/",
        RESOURCE_GROUP_VIEWS.delete_obj_instance,
        name="delete_resource_pool",
    ),
    path(
        "resource_pools/view/<int:id>/",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="view_resource_pool",
    ),
    path(
        "resource_pools/view/<int:id>/edit=<str:edit>",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="edit_resource_pool",
    ),
    path(
        "resource-pools/view/<int:id>/field=<str:field>",
        RESOURCE_GROUP_VIEWS.show_model_form,
        name="resource_pool_dependencies",
    ),
]
