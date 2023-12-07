from django.urls import path

from . import views  # Import the get_jobs view

urlpatterns = [
    path("jobs/new/", views.show_job_form, name="job_form"),
    path("job-create/", views.save_job_form, name="job_create"),
    path("jobs/", views.show_all_jobs, name="job"),
    path("jobs/delete/<int:id>/", views.request_job_delete, name="delete_job"),
    path("jobs/view/<int:id>/", views.show_job_form, name="view_job"),
    path("jobs/view/<int:id>/edit=<str:edit>", views.show_job_form, name="edit_job"),
]
