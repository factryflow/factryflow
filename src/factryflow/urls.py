from api.api import api
from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.views.generic import TemplateView


def home(request):
    return render(request, "base/main.html")


def job(request):
    return render(request, "base/job/main.html")


def task(request):
    return render(request, "base/task/main.html")


def jobform(request):
    return render(request, "base/job/form.html")


def taskform(request):
    return render(request, "base/task/form.html")


def chart(request):
    return render(request, "base/chart/main.html")


def settingsPage(request):
    return render(request, "base/settings/form.html")


def operatorPage(request):
    return render(request, "base/operatorview/main.html")


def operatorIssuePage(request):
    return render(request, "base/operatorview/issuepage.html")


def operatorOEPage(request):
    return render(request, "base/operatorview/operationexception.html")


if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path("", home, name="home"),
    path("chart/", chart, name="chart"),
    path("settings/", settingsPage, name="settings"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("invitations/", include("invitations.urls"), name="invitations"),
    path("operatorview/", operatorPage, name="operatorPage"),
    path("operatorview/issue/", operatorIssuePage, name="operatorIssuePage"),
    path("operatorview/operationexception/", operatorOEPage, name="operatorOEPage"),
    path("", include("users.urls", namespace="users")),
    path("", include("job_manager.urls")),
    path("", include("resource_manager.urls")),
    path("", include("resource_calendar.urls")),
    path("", include("resource_assigner.urls")),
    path("", include("issue.urls")),
    path("", include("scheduler.urls")),
    path("", include("common.urls")),
    path("api/", api.urls),
    path("", TemplateView.as_view(template_name="index.html")),
]

if settings.DEBUG == "TRUE":
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
