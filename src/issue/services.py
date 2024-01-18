from common.services import model_update
from common.utils import get_object
from django.core.files import File
from django.db import transaction
from job_manager.models.task import Task

from .models import Comment, Issue

# ------------------------------------------------------------------------------
# Issue Service
# ------------------------------------------------------------------------------


class IssueService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(
        self, *, title: str, description: str, thumbnail: File, status: str, task: Task
    ) -> Issue:
        issue = Issue.objects.create(
            title=title,
            description=description,
            thumbnail=thumbnail,
            status=status,
            task=task,
        )
        issue.full_clean()
        issue.save()

        return issue

    @transaction.atomic
    def update(self, *, issue: Issue, data: dict) -> Issue:
        fields = ["title", "description", "thumbnail", "status", "task"]

        issue, _ = model_update(instance=issue, fields=fields, data=data)
        return issue

    @transaction.atomic
    def delete(self, *, issue: Issue) -> None:
        issue.delete()


# ------------------------------------------------------------------------------
# Comment Service
# ------------------------------------------------------------------------------


class CommentService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(self, *, created_by: str, body: str, issue: Issue) -> Issue:
        comment = Comment.objects.create(created_by=created_by, body=body, issue=issue)
        comment.full_clean()
        comment.save()

        return comment

    @transaction.atomic
    def update(self, *, comment: Comment, data: dict) -> Comment:
        fields = ["updated_by", "body"]

        comment, _ = model_update(instance=comment, fields=fields, data=data)
        return comment

    @transaction.atomic
    def delete(self, *, comment: Comment) -> None:
        comment.delete()


# TODO: Should be moved inside the IssueService class?
def issue_create_or_update(issue_data: dict, issue_type: str):
    """
    Create or update issue based on issue type (Tag)
    """

    for issue_dict in issue_data:
        issue_id = issue_dict.get("id")
        issue_instance = get_object(model_or_queryset=Issue, id=issue_id)

        # TODO: Integrating the Taggit model
        if issue_instance:
            IssueService().update(instance=issue_instance, data=issue_dict)
        else:
            IssueService().create(
                title=issue_dict.get("title"),
                description=issue_dict.get("description"),
                thumbnail=issue_dict.get("thumbnail"),
                status=issue_dict.get("status"),
                task=issue_dict.get("task"),
            )


def issue_delete(id: int):
    """
    Delete issue based on id
    """
    issue = get_object(model_or_queryset=Issue, id=id)
    IssueService().delete(instance=issue)


# TODO: Should be moved inside the CommentService class?
def comment_create_or_update(comment_data: dict, issue_id: int):
    """
    Create or update comment
    """
    for comment_dict in comment_data:
        # Assigning post to the comment
        comment_id = comment_dict.get("issue", issue_id)
        comment_instance = get_object(model_or_queryset=Comment, id=comment_id)

        if comment_instance:
            CommentService().update(instance=comment_instance, data=comment_dict)
        else:
            CommentService().create(
                created_by=comment_dict.get("created_by"),
                body=comment_dict.get("body"),
                issue=comment_dict.get("issue", issue_id),
            )
