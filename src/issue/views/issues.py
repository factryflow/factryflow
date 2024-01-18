from common.utils.views import add_notification_headers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from taggit.models import Tag

from ..forms import IssueForm
from ..models import Issue
from ..selectors import issue_list
from ..services import issue_create_or_update, issue_delete

# ------------------------------------------------------------------------------
# Issue Views
# ------------------------------------------------------------------------------


class IssueCardView:
    """
    Class representing a view for displaying issues in a card format.
    """

    def __init__(self, search_query: dict = None):
        """
        Initialization of the class with optional filtering parameters.
        """
        self.issues = issue_list()
        self.search_query = search_query

    @property
    def filter_issues(self):
        """
        Property to get filtered issue list based on search query
        """
        issues = self.issues
        if self.search_query:
            issues = [
                issue
                for issue in issues
                if self.search_query.lower() in issue.title.lower()
                or self.search_query.lower() in issue.description.lower()
                or self.search_query.lower() in issue.task.lower()
                or str(self.search_query) in str(issue.id)
            ]
        return issues

    @property
    def card_details(self):
        """
        Property to get details for each card
        """
        return [
            [
                issue.title,
                issue.description,
                f'<span class="{self.get_status_colored_text(issue.tags)} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">{issue.tags}</span>',
                issue.thumbnail,
                issue.created_at,
                issue.created_by,
            ]
            for issue in self.filter_issues
        ]

    def _get_status_colored_text(self, issue_tags):
        """
        Private method to get colored text based on tagged issue.
        """
        tailwind_classes = {
            "open": "bg-haxred text-[#FF4D4F]",
            "closed": "bg-haxgreen text-[#52C41A]",
        }
        return tailwind_classes.get(issue_tags)


def show_issues_list(request, tag_slug=None):
    """
    View for displaying a list of issues with optional filtering.
    """
    search_query = request.GET.get("query", None)
    issue_list = IssueCardView(search_query=search_query)
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        issue_list = issue_list.filter(tags__in=[tag])

    # Pagination with 10 issues per page
    paginator = Paginator(issue_list, 10)
    page_number = request.GET.get("page", 1)

    try:
        issues = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        issues = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        issues = paginator.page(paginator.num_pages)

    template_name = (
        "objects/operator_view/list.html#partial-card-template"
        if "HX-Request" in request.headers
        else "objects/operator_view/list.html"
    )

    return render(request, template_name, {"issues": issues.card_details})


def show_issue_form(request, id: int = None, edit: str = ""):
    """
    View function to display a form for an issue. This can be used for both creating and editing an issue.
    """
    form_action_url = "/issue-create/"

    if id:
        issue = get_object_or_404(Issue, id=id)
        form = IssueForm(instance=issue)
        page_label = issue.title

        if edit != "T":
            view_mode = True
            form_label = "Issue Details"
            button_text = "Edit"
            edit_url = reverse("edit_issue", args=[id, "T"])

            # Make all form fields read-only
            for field in form.fields.values():
                field.widget.attrs["readonly"] = True

        else:
            button_text = "Save"
            form_label = "Issue Details"
            view_mode = False

    else:
        form = IssueForm()
        button_text = "Create"
        view_mode = False
        form_label = "New Issue Details"
        page_label = "New Issue"

    context = {
        "form": form,
        "view_mode": view_mode,
        "form_label": form_label,
        "button_text": button_text,
        "form_action_url": form_action_url,
        "id": id if id else None,
        "edit_url": edit_url
        if "edit_url" in locals()
        else "#",  # redirect to active operator view page
        "page_label": page_label,
    }

    return render(
        request,
        "objects/operator_view/details.html",
        context,
    )


@require_http_methods(["POST"])
def save_issue_form(request, id: int = None):
    """
    Handle POST request to create or update using Django form and service.
    """
    # Get the issue instance if updating, else None
    issue_instance = get_object_or_404(Issue, id=id) if id else None

    # Instantiate the form with POST data and optionally the issue instance
    form = IssueForm(request.POST, instance=issue_instance)

    # id = request.POST.get("id") -> Possibly Redundant

    if form.is_valid():
        # Extract data from the form
        issue_data = form.cleaned_data
        issue_data["id"] = id
        # TODO: Looking for a way to properly handle update/create of tags
        issue_type = issue_data["tags"]

        issue_create_or_update(issue_data=issue_data, issue_type=issue_type)

        form = IssueForm()
        response = render(
            request,
            "objects/operator_view/details.html#partial-form",
            {"form": form, "button_text": "Add Issue", "form_label": "Issue Details"},
        )

        if request.htmx:
            headers = {"HX-Redirect": reverse("issue")}
            response = HttpResponse(status=204, headers=headers)
            add_notification_headers(response, "Issue created successfully!", "success")


def request_issue_delete(request, id: int):
    """
    Handle issue deletion request. Deletes the issue based on a given ID,
    retrieves the updated issue list, and returns a response with a notification.
    """
    issue_delete(id=id)
    cards = IssueCardView()
    response = render(
        request,
        "objects/operator_view/list.html#partial-card-template",
        {"issues": cards.card_details},
    )
    add_notification_headers(response, "Issue deleted successfully!", "success")
    return response
