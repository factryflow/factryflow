from django.urls import path

from .views import (
    JOB_VIEWS,
    TASK_VIEWS,
    DEPENDENCY_VIEWS,
    JOB_TYPE_VIEWS,
    TASK_TYPE_VIEWS,
    DEPENDENCY_TYPE_VIEWS,
    WORK_CENTER_VIEWS,
    ITEM_VIEWS,
)

urlpatterns = [
    # work center urls
    path(
        "work-center/new/", WORK_CENTER_VIEWS.show_model_form, name="work_center_form"
    ),
    path(
        "work-center-create/",
        WORK_CENTER_VIEWS.create_or_update_model_instance,
        name="work_center_create",
    ),
    path("work-centers/", WORK_CENTER_VIEWS.get_all_instances, name="work_centers"),
    path(
        "work-center/delete/<int:id>/",
        WORK_CENTER_VIEWS.delete_obj_instance,
        name="delete_work_center",
    ),
    path(
        "work-center/view/<int:id>/",
        WORK_CENTER_VIEWS.show_model_form,
        name="view_work_center",
    ),
    path(
        "work-center/view/<int:id>/edit=<str:edit>",
        WORK_CENTER_VIEWS.show_model_form,
        name="edit_work_center",
    ),
    path(
        "work-center/view/<int:id>/field=<str:field>",
        WORK_CENTER_VIEWS.show_model_form,
        name="work_center_dependencies",
    ),
    # jobs urls
    path("job/new/", JOB_VIEWS.show_model_form, name="job_form"),
    path("job-create/", JOB_VIEWS.create_or_update_model_instance, name="job_create"),
    path("jobs/", JOB_VIEWS.get_all_instances, name="jobs"),
    path("job/delete/<int:id>/", JOB_VIEWS.delete_obj_instance, name="delete_job"),
    path("job/view/<int:id>/", JOB_VIEWS.show_model_form, name="view_job"),
    path(
        "job/view/<int:id>/edit=<str:edit>", JOB_VIEWS.show_model_form, name="edit_job"
    ),
    path(
        "job/view/<int:id>/field=<str:field>",
        JOB_VIEWS.show_model_form,
        name="job_dependencies",
    ),
    # job_type urls
    path("job-type/new/", JOB_TYPE_VIEWS.show_model_form, name="job_type_form"),
    path(
        "job-type-create/",
        JOB_TYPE_VIEWS.create_or_update_model_instance,
        name="job_type_create",
    ),
    path("job-types/", JOB_TYPE_VIEWS.get_all_instances, name="job_types"),
    path(
        "job-type/delete/<int:id>/",
        JOB_TYPE_VIEWS.delete_obj_instance,
        name="delete_job_type",
    ),
    path(
        "job-type/view/<int:id>/",
        JOB_TYPE_VIEWS.show_model_form,
        name="view_job_type",
    ),
    path(
        "job-type/view/<int:id>/edit=<str:edit>",
        JOB_TYPE_VIEWS.show_model_form,
        name="edit_job_type",
    ),
    path(
        "job-type/view/<int:id>/field=<str:field>",
        JOB_TYPE_VIEWS.show_model_form,
        name="job_type_dependencies",
    ),
    # tasks urls
    path("task/new/", TASK_VIEWS.show_model_form, name="task_form"),
    path(
        "task-create/", TASK_VIEWS.create_or_update_model_instance, name="task_create"
    ),
    path("tasks/", TASK_VIEWS.get_all_instances, name="tasks"),
    path("task/delete/<int:id>/", TASK_VIEWS.delete_obj_instance, name="delete_task"),
    path("task/view/<int:id>/", TASK_VIEWS.show_model_form, name="view_task"),
    path(
        "task/view/<int:id>/edit=<str:edit>",
        TASK_VIEWS.show_model_form,
        name="edit_task",
    ),
    path(
        "task/view/<int:id>/field=<str:field>",
        TASK_VIEWS.show_model_form,
        name="task_dependencies",
    ),
    # task type urls
    path("task-type/new/", TASK_TYPE_VIEWS.show_model_form, name="task_type_form"),
    path(
        "task-type-create/",
        TASK_TYPE_VIEWS.create_or_update_model_instance,
        name="task_type_create",
    ),
    path("task-types/", TASK_TYPE_VIEWS.get_all_instances, name="task_types"),
    path(
        "task-type/delete/<int:id>/",
        TASK_TYPE_VIEWS.delete_obj_instance,
        name="delete_task_type",
    ),
    path(
        "task-type/view/<int:id>/",
        TASK_TYPE_VIEWS.show_model_form,
        name="view_task_type",
    ),
    path(
        "task-type/view/<int:id>/edit=<str:edit>",
        TASK_TYPE_VIEWS.show_model_form,
        name="edit_task_type",
    ),
    path(
        "task-type/view/<int:id>/field=<str:field>",
        TASK_TYPE_VIEWS.show_model_form,
        name="task_type_dependencies",
    ),
    # dependencies urls
    path("dependency/new/", DEPENDENCY_VIEWS.show_model_form, name="dependency_form"),
    path(
        "dependency-create/",
        DEPENDENCY_VIEWS.create_or_update_model_instance,
        name="dependency_create",
    ),
    path("dependencys/", DEPENDENCY_VIEWS.get_all_instances, name="dependencys"),
    path(
        "dependency/delete/<int:id>/",
        DEPENDENCY_VIEWS.delete_obj_instance,
        name="delete_dependency",
    ),
    path(
        "dependency/view/<int:id>/",
        DEPENDENCY_VIEWS.show_model_form,
        name="view_dependency",
    ),
    path(
        "dependency/view/<int:id>/edit=<str:edit>",
        DEPENDENCY_VIEWS.show_model_form,
        name="edit_dependency",
    ),
    path(
        "dependency/view/<int:id>/field=<str:field>",
        DEPENDENCY_VIEWS.show_model_form,
        name="dependency_dependencies",
    ),
    # dependency type urls
    path(
        "dependency-type/new/",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="dependency_type_form",
    ),
    path(
        "dependency-type-create/",
        DEPENDENCY_TYPE_VIEWS.create_or_update_model_instance,
        name="dependency_type_create",
    ),
    path(
        "dependency-types/",
        DEPENDENCY_TYPE_VIEWS.get_all_instances,
        name="dependency_types",
    ),
    path(
        "dependency-type/delete/<int:id>/",
        DEPENDENCY_TYPE_VIEWS.delete_obj_instance,
        name="delete_dependency_type",
    ),
    path(
        "dependency-type/view/<int:id>/",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="view_dependency_type",
    ),
    path(
        "dependency-type/view/<int:id>/edit=<str:edit>",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="edit_dependency_type",
    ),
    path(
        "dependency-type/view/<int:id>/field=<str:field>",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="dependency_type_dependencies",
    ),
    # item urls
    path("item/new/", ITEM_VIEWS.show_model_form, name="item_form"),
    path(
        "item-create/", ITEM_VIEWS.create_or_update_model_instance, name="item_create"
    ),
    path("items/", ITEM_VIEWS.get_all_instances, name="items"),
    path("items/delete/<int:id>/", ITEM_VIEWS.delete_obj_instance, name="delete_item"),
    path("item/view/<int:id>/", ITEM_VIEWS.show_model_form, name="view_item"),
    path(
        "item/view/<int:id>/edit=<str:edit>",
        ITEM_VIEWS.show_model_form,
        name="edit_item",
    ),
    path(
        "item/view/<int:id>/field=<str:field>",
        ITEM_VIEWS.show_model_form,
        name="item_dependencies",
    ),
]
