from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def home(request):
    return render(request, "base/main.html")


def job(request):
    return render(request, "base/job/main.html")


def jobform(request):
    return render(request, "base/job/form.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("", include("job_manager.urls")),
]
