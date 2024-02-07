from django.urls import path

from .views import JOB_VIEWS, TASK_VIEWS, DEPENDENCY_VIEWS

urlpatterns = [
    # jobs urls
    path("jobs/new/", JOB_VIEWS.show_model_form, name="job_form"),
    path("job-create/", JOB_VIEWS.create_or_update_model_instance, name="job_create"),
    path("jobs/", JOB_VIEWS.get_all_instances, name="job"),
    path("jobs/delete/<int:id>/", JOB_VIEWS.delete_obj_instance, name="delete_job"),
    path("jobs/view/<int:id>/", JOB_VIEWS.show_model_form, name="view_job"),
    path(
        "jobs/view/<int:id>/edit=<str:edit>", JOB_VIEWS.show_model_form, name="edit_job"
    ),
    # tasks urls
    path("task/new/", TASK_VIEWS.show_model_form, name="task_form"),
    path(
        "task-create/", TASK_VIEWS.create_or_update_model_instance, name="task_create"
    ),
    path("task/", TASK_VIEWS.get_all_instances, name="task"),
    path("task/delete/<int:id>/", TASK_VIEWS.delete_obj_instance, name="delete_task"),
    path("task/view/<int:id>/", TASK_VIEWS.show_model_form, name="view_task"),
    path(
        "task/view/<int:id>/edit=<str:edit>",
        TASK_VIEWS.show_model_form,
        name="edit_task",
    ),

    # dependencies urls
    path("dependency/new/", DEPENDENCY_VIEWS.show_model_form, name="dependency_form"),
    path(
        "dependency-create/",
        DEPENDENCY_VIEWS.create_or_update_model_instance,
        name="dependency_create",
    ),
    path("dependency/", DEPENDENCY_VIEWS.get_all_instances, name="dependency"),
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
]
