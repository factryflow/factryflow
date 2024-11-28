from common.utils.ordered_models import change_obj_priority
from common.utils.views import add_notification_headers
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from resource_assigner.models import AssigmentRule


# ------------------------------------------------------------------------------
# Ordered Model APIs to manage the order of the rules based on the work center
# ------------------------------------------------------------------------------


def change_assignment_rule_priority(request, id: int, direction: str):
    """
    Move the rule up or down in the order.

    Parameters:
    -----------
        id: int - The id of the rule.
        direction: str - The direction to move the rule. It can be either "up" or "down".

    Returns:
    --------
        dict: A dictionary containing the message of the operation.
    """

    response = HttpResponse(status=302)
    response["Location"] = reverse("assigment_rules")

    if direction not in ["up", "down"]:
        response = HttpResponse(status=400)
        message = "Invalid direction. Use 'up' or 'down'."
        add_notification_headers(response, message, "error")
        return response

    try:
        change_obj_priority(model_class=AssigmentRule, id=id, direction=direction)

        if request.htmx:
            response = render(
                request,
                "objects/list.html#all-assigment_rules-table",
                {"rows": AssigmentRule.objects.all().order_by("order")},
            )
            return response

        return response

    except AssigmentRule.DoesNotExist:
        response = HttpResponse(status=404)
        message = "Rule not found."
        add_notification_headers(response, message, "error")
        return response

    except Exception as e:
        message = f"An error occurred: {str(e)}"
        add_notification_headers(response, message, "error")
        return response
