from django.urls import path

from .views import *

urlpatterns = [
    # resources urls
    path("resources/new/", RESOURCE_VIEWS.show_model_form, name="resource_form"),
    path(
        "resource-create/", RESOURCE_VIEWS.create_or_update_model_instance, name="resource_create"
    ),
    path("resources/", RESOURCE_VIEWS.get_all_instances, name="resource"),
    path("resources/delete/<int:id>/", RESOURCE_VIEWS.delete_obj_instance, name="delete_resource"),
    path("resources/view/<int:id>/", RESOURCE_VIEWS.show_model_form, name="view_resource"),
    path(
        "resources/view/<int:id>/edit=<str:edit>", RESOURCE_VIEWS.show_model_form, name="edit_resource"
    ),
    
    # resource pool urls
    path("resource_pools/new/", RESOURCE_POOL_VIEWS.show_model_form, name="resource_pool_form"),
    path(
        "resource_pool-create/",
        RESOURCE_POOL_VIEWS.create_or_update_model_instance,
        name="resource_pool_create",
    ),
    path("resource-pools/", RESOURCE_POOL_VIEWS.get_all_instances, name="resource_pool"),
    path(
        "resource_pools/delete/<int:id>/",
        RESOURCE_POOL_VIEWS.delete_obj_instance,
        name="delete_resource_pool",
    ),
    path(
        "resource_pools/view/<int:id>/",
        RESOURCE_POOL_VIEWS.show_model_form,
        name="view_resource_pool",
    ),
    path(
        "resource_pools/view/<int:id>/edit=<str:edit>",
        RESOURCE_POOL_VIEWS.show_model_form,
        name="edit_resource_pool",
    ),
    path(
        "resource-pools/view/<int:id>/field=<str:field>",
        RESOURCE_POOL_VIEWS.show_model_form,
        name="resource_pool_dependencies",
    ),

    # work unit urls
    path("work_units/new/", WORK_UNIT_VIEWS.show_model_form, name="work_unit_form"),
    path(
        "work_unit-create/", WORK_UNIT_VIEWS.create_or_update_model_instance, name="work_unit_create"
    ),
    path("work_units/", WORK_UNIT_VIEWS.get_all_instances, name="work_unit"),
    path("work_units/delete/<int:id>/", WORK_UNIT_VIEWS.delete_obj_instance, name="delete_work_unit"),
    path("work_units/view/<int:id>/", WORK_UNIT_VIEWS.show_model_form, name="view_work_unit"),
    path(
        "work_units/view/<int:id>/edit=<str:edit>",
        WORK_UNIT_VIEWS.show_model_form,
        name="edit_work_unit",
    ),
]