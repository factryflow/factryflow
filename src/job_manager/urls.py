from django.urls import path

from .views import JOB_VIEWS, TASK_VIEWS, DEPENDENCY_VIEWS, JOB_TYPE_VIEWS, TASK_TYPE_VIEWS, DEPENDENCY_TYPE_VIEWS, WORK_CENTER_VIEWS, ITEM_VIEWS

urlpatterns = [
    # work center urls
    path("work-centers/new/", WORK_CENTER_VIEWS.show_model_form, name="work_center_form"),
    path(
        "work_center-create/",
        WORK_CENTER_VIEWS.create_or_update_model_instance,
        name="work_center_create",
    ),
    path("work-centers/", WORK_CENTER_VIEWS.get_all_instances, name="work_center"),
    path(
        "work_centers/delete/<int:id>/",
        WORK_CENTER_VIEWS.delete_obj_instance,
        name="delete_work_center",
    ),
    path(
        "work-centers/view/<int:id>/",
        WORK_CENTER_VIEWS.show_model_form,
        name="view_work_center",
    ),
    path(
        "work-centers/view/<int:id>/edit=<str:edit>",
        WORK_CENTER_VIEWS.show_model_form,
        name="edit_work_center",
    ),
    

    # jobs urls
    path("jobs/new/", JOB_VIEWS.show_model_form, name="job_form"),
    path("job-create/", JOB_VIEWS.create_or_update_model_instance, name="job_create"),
    path("jobs/", JOB_VIEWS.get_all_instances, name="job"),
    path("jobs/delete/<int:id>/", JOB_VIEWS.delete_obj_instance, name="delete_job"),
    path("jobs/view/<int:id>/", JOB_VIEWS.show_model_form, name="view_job"),
    path(
        "jobs/view/<int:id>/edit=<str:edit>", JOB_VIEWS.show_model_form, name="edit_job"
    ),
    path(
        "jobs/view/<int:id>/field=<str:field>",
        JOB_VIEWS.show_model_form,
        name="job_dependencies",
    ),

    # job_type urls
    path("job-types/new/", JOB_TYPE_VIEWS.show_model_form, name="job_type_form"),
    path(
        "job_type-create/",
        JOB_TYPE_VIEWS.create_or_update_model_instance,
        name="job_type_create",
    ),
    path("job-types/", JOB_TYPE_VIEWS.get_all_instances, name="job_type"),
    path(
        "job_types/delete/<int:id>/",
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

    # tasks urls
    path("tasks/new/", TASK_VIEWS.show_model_form, name="task_form"),
    path(
        "task-create/", TASK_VIEWS.create_or_update_model_instance, name="task_create"
    ),
    path("tasks/", TASK_VIEWS.get_all_instances, name="task"),
    path("tasks/delete/<int:id>/", TASK_VIEWS.delete_obj_instance, name="delete_task"),
    path("tasks/view/<int:id>/", TASK_VIEWS.show_model_form, name="view_task"),
    path(
        "tasks/view/<int:id>/edit=<str:edit>",
        TASK_VIEWS.show_model_form,
        name="edit_task",
    ),
    path(
        "tasks/view/<int:id>/field=<str:field>",
        TASK_VIEWS.show_model_form,
        name="task_dependencies",
    ),

    # task type urls
    path("task-types/new/", TASK_TYPE_VIEWS.show_model_form, name="task_type_form"),
    path(
        "task_type-create/",
        TASK_TYPE_VIEWS.create_or_update_model_instance,
        name="task_type_create",
    ),
    path("task-types/", TASK_TYPE_VIEWS.get_all_instances, name="task_type"),
    path(
        "task_types/delete/<int:id>/",
        TASK_TYPE_VIEWS.delete_obj_instance,
        name="delete_task_type",
    ),
    path(
        "task-types/view/<int:id>/",
        TASK_TYPE_VIEWS.show_model_form,
        name="view_task_type",
    ),
    path(
        "task-types/view/<int:id>/edit=<str:edit>",
        TASK_TYPE_VIEWS.show_model_form,
        name="edit_task_type",
    ),


    # dependencies urls
    path("dependencys/new/", DEPENDENCY_VIEWS.show_model_form, name="dependency_form"),
    path(
        "dependency-create/",
        DEPENDENCY_VIEWS.create_or_update_model_instance,
        name="dependency_create",
    ),
    path("dependencys/", DEPENDENCY_VIEWS.get_all_instances, name="dependency"),
    path(
        "dependencys/delete/<int:id>/",
        DEPENDENCY_VIEWS.delete_obj_instance,
        name="delete_dependency",
    ),
    path(
        "dependencys/view/<int:id>/",
        DEPENDENCY_VIEWS.show_model_form,
        name="view_dependency",
    ),
    path(
        "dependencys/view/<int:id>/edit=<str:edit>",
        DEPENDENCY_VIEWS.show_model_form,
        name="edit_dependency",
    ),
    path(
        "dependencys/view/<int:id>/field=<str:field>",
        DEPENDENCY_VIEWS.show_model_form,
        name="dependency_dependencies",
    ),

    # dependency type urls
    path(
        "dependency-types/new/",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="dependency_type_form",
    ),
    path(
        "dependency_type-create/",
        DEPENDENCY_TYPE_VIEWS.create_or_update_model_instance,
        name="dependency_type_create",
    ),
    path(
        "dependency-types/",
        DEPENDENCY_TYPE_VIEWS.get_all_instances,
        name="dependency_type",
    ),
    path(
        "dependency_types/delete/<int:id>/",
        DEPENDENCY_TYPE_VIEWS.delete_obj_instance,
        name="delete_dependency_type",
    ),
    path(
        "dependency-types/view/<int:id>/",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="view_dependency_type",
    ),
    path(
        "dependency-types/view/<int:id>/edit=<str:edit>",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="edit_dependency_type",
    ),

    # item urls
    path("items/new/", ITEM_VIEWS.show_model_form, name="item_form"),
    path("item-create/", ITEM_VIEWS.create_or_update_model_instance, name="item_create"),
    path("items/", ITEM_VIEWS.get_all_instances, name="item"),
    path("items/delete/<int:id>/", ITEM_VIEWS.delete_obj_instance, name="delete_item"),
    path("items/view/<int:id>/", ITEM_VIEWS.show_model_form, name="view_item"),
    path("items/view/<int:id>/edit=<str:edit>", ITEM_VIEWS.show_model_form, name="edit_item"),
]
