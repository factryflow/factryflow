import json

from django.http import HttpResponse


def add_notification_headers(
    response: HttpResponse, notification_content: str, notification_type: str = "info"
) -> HttpResponse:
    """
    Adds a custom 'hx-trigger' header to the HttpResponse for triggering a notification.
    """
    allowed_types = ["info", "success", "error"]

    # Validate notification type
    if notification_type not in allowed_types:
        raise ValueError(
            f"Invalid notification type: {notification_type}. Allowed types are {allowed_types}"
        )

    notification_data = json.dumps(
        {
            "notify": {
                "content": notification_content,
                "type": notification_type,
            }
        }
    )

    response["hx-trigger"] = notification_data
    return response
