from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

# ------------------------------------------------------------------------------
# JOB-TASK gantt-chart View
# ------------------------------------------------------------------------------


def dashboard_gantt_chart_view(request, gantt_type: str = "job", home: str = "true"):
    """
    Dashboard
        Job Task gantt chart data view

    Args:
        request (HttpRequest): The HTTP request object.
        gantt_type (str): The type of Gantt chart to display. Defaults to "job".

    Returns:
        HttpResponse: The HTTP response with the rendered Gantt chart view.
    """
    if request.user.require_password_change:
        return redirect(reverse("users:change_password"))

    if "HX-Request" in request.headers and home == "false":
        if gantt_type == "job":
            return render(
                request,
                "dashboard/job_task_gantt.html",
                {
                    "gantt_chart_title": "Job Task",
                    "API_BASE_URL": settings.API_BASE_URL,
                },
            )
        else:
            return render(
                request,
                "dashboard/resource_gantt.html",
                {
                    "gantt_chart_title": "Resource",
                    "API_BASE_URL": settings.API_BASE_URL,
                },
            )

    return render(
        request,
        "dashboard/base.html",
        {
            "gantt_chart_title": "Job Task",
            "gantt_chart": "dashboard/job_task_gantt.html",
            "API_BASE_URL": settings.API_BASE_URL,
        },
    )
