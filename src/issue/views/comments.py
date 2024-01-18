from common.utils.views import add_notification_headers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..forms import CommentForm
from ..models import Issue
from ..services import comment_create_or_update

# ------------------------------------------------------------------------------
# Comment Views
# ------------------------------------------------------------------------------


@require_http_methods(["POST"])
def post_comment(request, id: int = None):
    """
    View to post a comment on an issue
    """
    issue_instance = get_object_or_404(Issue, id=id, status=Issue.status.PUBLISHED)
    comment_data = None

    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment_data = form.save(commit=False)

        comment_create_or_update(comment_data=comment_data, issue_id=issue_instance)

        form = CommentForm()
        response = render(
            request,
            "objects/operator_view/comments.html#partial-form",
            {"form": form, "button_text": "Add Comment", "form_label": "Comment"},
        )

        if request.htmx:
            headers = {"HX-Redirect": reverse("comment")}
            response = HttpResponse(status=204, headers=headers)
            add_notification_headers(
                response, "Comment created successfully!", "success"
            )
