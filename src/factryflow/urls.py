from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, "base/main.html")


@login_required(login_url='/accounts/login/')
def job(request):
    return render(request, "base/job/main.html")


@login_required(login_url='/accounts/login/')
def task(request):
    return render(request, "base/task/main.html")


@login_required(login_url='/accounts/login/')
def jobform(request):
    return render(request, "base/job/form.html")


@login_required(login_url='/accounts/login/')
def taskform(request):
    return render(request, "base/task/form.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("", include("job_manager.urls")),
]
