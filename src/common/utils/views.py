import json

from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


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


def convert_datetime_to_readable_string(datetime: str) -> str:
    """
    Converts a datetime string to a human-readable string.
    """
    return datetime.strftime("%B %d, %Y %I:%M %p")


def convert_date_to_readable_string(date: str) -> str:
    """
    Converts a date string to a human-readable string.
    """
    return date.strftime("%B %d, %Y")


def convert_timestamp(datetime: str) -> str:
    """
    Converts a datetime object to "DD-MM-YYYY HH:MM"
    """
    return datetime.strftime("%d-%m-%Y %H:%M")


def convert_date(datetime: str) -> str:
    """
    Converts a datetime object to "DD-MM-YYYY"
    """
    return datetime.strftime("%d-%m-%Y")


def paginate_data(all_instances, page_number, num_of_rows_per_page=25):
    """
    Paginates the data and returns the paginated data along with the number of pages and total instances count.
    """
    paginator = Paginator(all_instances, num_of_rows_per_page)
    num_pages = paginator.num_pages
    total_instances_count = paginator.count

    try:
        paginated_instances = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_instances = paginator.page(1)
    except EmptyPage:
        paginated_instances = paginator.page(paginator.num_pages)
    return paginated_instances, num_pages, total_instances_count
