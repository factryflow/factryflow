from django.urls import path

from .views import JOB_VIEWS

urlpatterns = [
    path("jobs/new/", JOB_VIEWS.show_model_form, name="job_form"),
    path("job-create/", JOB_VIEWS.create_or_update_model_instance, name="job_create"),
    path("jobs/", JOB_VIEWS.get_all_instances, name="job"),
    path("jobs/delete/<int:id>/", JOB_VIEWS.delete_obj_instance, name="delete_job"),
    path("jobs/view/<int:id>/", JOB_VIEWS.show_model_form, name="view_job"),
    path("jobs/view/<int:id>/edit=<str:edit>", JOB_VIEWS.show_model_form, name="edit_job"),
]
