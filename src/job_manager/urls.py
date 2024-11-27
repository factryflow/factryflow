from django.urls import path

from job_manager.api.chart_data import JobGanttAPIView, ResourceGanttAPIView

from job_manager.views import (
    DEPENDENCY_TYPE_VIEWS,
    DEPENDENCY_VIEWS,
    ITEM_VIEWS,
    JOB_TYPE_VIEWS,
    JOB_VIEWS,
    TASK_TYPE_VIEWS,
    TASK_VIEWS,
    WORK_CENTER_VIEWS,
    dashboard_gantt_chart_view,
    job_prioritization_view,
)

urlpatterns = [
    # work center urls
    path(
        "work-centers/new/", WORK_CENTER_VIEWS.show_model_form, name="work_centers_form"
    ),
    path(
        "work-centers-create/",
        WORK_CENTER_VIEWS.create_or_update_model_instance,
        name="work_centers_create",
    ),
    path("work-centers/", WORK_CENTER_VIEWS.get_all_instances, name="work_centers"),
    path(
        "work-centers/delete/<int:id>/",
        WORK_CENTER_VIEWS.delete_obj_instance,
        name="delete_work_centers",
    ),
    path(
        "work-centers/view/<int:id>/",
        WORK_CENTER_VIEWS.show_model_form,
        name="view_work_centers",
    ),
    path(
        "work-centers/view/<int:id>/edit=<str:edit>",
        WORK_CENTER_VIEWS.show_model_form,
        name="edit_work_centers",
    ),
    path(
        "work-centers/view/<int:id>/field=<str:field>",
        WORK_CENTER_VIEWS.show_model_form,
        name="work_center_relationships",
    ),
    # jobs urls
    path("jobs/new/", JOB_VIEWS.show_model_form, name="jobs_form"),
    path("jobs-create/", JOB_VIEWS.create_or_update_model_instance, name="jobs_create"),
    path("jobs/", JOB_VIEWS.get_all_instances, name="jobs"),
    path("jobs/delete/<int:id>/", JOB_VIEWS.delete_obj_instance, name="delete_jobs"),
    path("jobs/view/<int:id>/", JOB_VIEWS.show_model_form, name="view_jobs"),
    path(
        "jobs/view/<int:id>/edit=<str:edit>",
        JOB_VIEWS.show_model_form,
        name="edit_jobs",
    ),
    path(
        "jobs/view/<int:id>/field=<str:field>",
        JOB_VIEWS.show_model_form,
        name="jobs_relationships",
    ),
    # job prioritization
    path(
        "job-prioritization/",
        job_prioritization_view,
        name="job_prioritization",
    ),
    # job_type urls
    path("job-types/new/", JOB_TYPE_VIEWS.show_model_form, name="job_types_form"),
    path(
        "job-types-create/",
        JOB_TYPE_VIEWS.create_or_update_model_instance,
        name="job_types_create",
    ),
    path("job-types/", JOB_TYPE_VIEWS.get_all_instances, name="job_types"),
    path(
        "job-types/delete/<int:id>/",
        JOB_TYPE_VIEWS.delete_obj_instance,
        name="delete_job_types",
    ),
    path(
        "job-types/view/<int:id>/",
        JOB_TYPE_VIEWS.show_model_form,
        name="view_job_types",
    ),
    path(
        "job-types/view/<int:id>/edit=<str:edit>",
        JOB_TYPE_VIEWS.show_model_form,
        name="edit_job_types",
    ),
    path(
        "job-types/view/<int:id>/field=<str:field>",
        JOB_TYPE_VIEWS.show_model_form,
        name="job_types_relationships",
    ),
    # tasks urls
    path("tasks/new/", TASK_VIEWS.show_model_form, name="tasks_form"),
    path(
        "tasks-create/", TASK_VIEWS.create_or_update_model_instance, name="tasks_create"
    ),
    path("tasks/", TASK_VIEWS.get_all_instances, name="tasks"),
    path("tasks/delete/<int:id>/", TASK_VIEWS.delete_obj_instance, name="delete_tasks"),
    path("tasks/view/<int:id>/", TASK_VIEWS.show_model_form, name="view_tasks"),
    path(
        "tasks/view/<int:id>/edit=<str:edit>",
        TASK_VIEWS.show_model_form,
        name="edit_tasks",
    ),
    path(
        "tasks/view/<int:id>/field=<str:field>",
        TASK_VIEWS.show_model_form,
        name="tasks_relationships",
    ),
    # task type urls
    path("task-types/new/", TASK_TYPE_VIEWS.show_model_form, name="task_types_form"),
    path(
        "task-types-create/",
        TASK_TYPE_VIEWS.create_or_update_model_instance,
        name="task_types_create",
    ),
    path("task-types/", TASK_TYPE_VIEWS.get_all_instances, name="task_types"),
    path(
        "task-types/delete/<int:id>/",
        TASK_TYPE_VIEWS.delete_obj_instance,
        name="delete_task_types",
    ),
    path(
        "task-types/view/<int:id>/",
        TASK_TYPE_VIEWS.show_model_form,
        name="view_task_types",
    ),
    path(
        "task-types/view/<int:id>/edit=<str:edit>",
        TASK_TYPE_VIEWS.show_model_form,
        name="edit_task_types",
    ),
    path(
        "task-types/view/<int:id>/field=<str:field>",
        TASK_TYPE_VIEWS.show_model_form,
        name="task_types_relationships",
    ),
    # dependencies urls
    path(
        "dependencies/new/", DEPENDENCY_VIEWS.show_model_form, name="dependencies_form"
    ),
    path(
        "dependencies-create/",
        DEPENDENCY_VIEWS.create_or_update_model_instance,
        name="dependency_create",
    ),
    path("dependencies/", DEPENDENCY_VIEWS.get_all_instances, name="dependencies"),
    path(
        "dependencies/delete/<int:id>/",
        DEPENDENCY_VIEWS.delete_obj_instance,
        name="delete_dependencies",
    ),
    path(
        "dependencies/view/<int:id>/",
        DEPENDENCY_VIEWS.show_model_form,
        name="view_dependencies",
    ),
    path(
        "dependencies/view/<int:id>/edit=<str:edit>",
        DEPENDENCY_VIEWS.show_model_form,
        name="edit_dependencies",
    ),
    path(
        "dependencies/view/<int:id>/field=<str:field>",
        DEPENDENCY_VIEWS.show_model_form,
        name="dependency_relationships",
    ),
    # dependency type urls
    path(
        "dependency-types/new/",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="dependency_types_form",
    ),
    path(
        "dependency-types-create/",
        DEPENDENCY_TYPE_VIEWS.create_or_update_model_instance,
        name="dependency_types_create",
    ),
    path(
        "dependency-types/",
        DEPENDENCY_TYPE_VIEWS.get_all_instances,
        name="dependency_types",
    ),
    path(
        "dependency-types/delete/<int:id>/",
        DEPENDENCY_TYPE_VIEWS.delete_obj_instance,
        name="delete_dependency_types",
    ),
    path(
        "dependency-types/view/<int:id>/",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="view_dependency_types",
    ),
    path(
        "dependency-types/view/<int:id>/edit=<str:edit>",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="edit_dependency_types",
    ),
    path(
        "dependency-types/view/<int:id>/field=<str:field>",
        DEPENDENCY_TYPE_VIEWS.show_model_form,
        name="dependency_types_relationships",
    ),
    # item urls
    path("items/new/", ITEM_VIEWS.show_model_form, name="items_form"),
    path(
        "items-create/", ITEM_VIEWS.create_or_update_model_instance, name="items_create"
    ),
    path("items/", ITEM_VIEWS.get_all_instances, name="items"),
    path("items/delete/<int:id>/", ITEM_VIEWS.delete_obj_instance, name="delete_items"),
    path("items/view/<int:id>/", ITEM_VIEWS.show_model_form, name="view_items"),
    path(
        "items/view/<int:id>/edit=<str:edit>",
        ITEM_VIEWS.show_model_form,
        name="edit_items",
    ),
    path(
        "items/view/<int:id>/field=<str:field>",
        ITEM_VIEWS.show_model_form,
        name="items_relationships",
    ),
    path(
        "api/job/gantt",
        JobGanttAPIView.as_view(),
        name="job_gantt_api",
    ),
    path(
        "api/resource/gantt",
        ResourceGanttAPIView.as_view(),
        name="resource_gantt_api",
    ),
    path(
        "dashboard/gantt-type=<str:gantt_type>/home=<str:home>/",
        dashboard_gantt_chart_view,
        name="dashboard",
    ),
]
