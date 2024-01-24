from common.utils.services import get_object
from common.utils.views import add_notification_headers
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..forms import CommentForm
from ..models import Comment, Issue
from ..services import CommentService

# ------------------------------------------------------------------------------
# Comment Views
# ------------------------------------------------------------------------------


@require_http_methods(["POST"])
def post_comment(request, id: int = None):
    """
    View to post a comment on an issue
    """
    issue_instance = get_object(Issue, id=id, status=Issue.status.PUBLISHED)
    comment_instance = get_object(Comment, id=id)
    comment_data = None

    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment_data = form.save(commit=False)

        if comment_instance:
            CommentService().update(instance=comment_instance, data=comment_data)
        else:
            CommentService().create(
                body=comment_data.get("body"),
                issue=issue_instance,
            )

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
