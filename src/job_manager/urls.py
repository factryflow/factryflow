from django.urls import path

from . import views  # Import the get_jobs view

urlpatterns = [
    path("jobs/new/", views.show_job_form, name="job_form"),
    path("job-create/", views.save_job_form, name="job_create"),
]
