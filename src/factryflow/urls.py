from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def home(request):
    return render(request, "base/main.html")

def job(request):
    return render(request,"base/job/main.html")

def task(request):
    return render(request,"base/task/main.html")

def jobform(request):
    return render(request,"base/job/form.html")

def taskform(request):
    return render(request,"base/task/form.html")

urlpatterns = [
    path("", home, name="home"),
    path("job/",job, name="job"),
    path("job/form/",jobform, name="jobform"),
    path("task/",task,name="task"),
    path("task/form/",taskform,name="taskform"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
]
