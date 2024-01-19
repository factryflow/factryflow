from api.permission_checker import AbstractPermissionService
from common.services import model_update
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.db import transaction
from job_manager.models.task import Task

from .models import Comment, Issue

# ------------------------------------------------------------------------------
# Issue Service
# ------------------------------------------------------------------------------


class IssueService:
    def __init__(self, user) -> None:
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(
        self,
        *,
        title: str,
        description: str,
        thumbnail: File = None,
        status: str = "PB",
        task: Task,
    ) -> Issue:
        # check permissions for add issue
        if not self.permission_service.check_for_permission("add_issue"):
            raise PermissionDenied()

        issue = Issue.objects.create(
            title=title,
            description=description,
            thumbnail=thumbnail,
            status=status,
            task=task,
        )
        issue.full_clean()
        issue.save(user=self.user)

        return issue

    @transaction.atomic
    def update(self, *, issue: Issue, data: dict) -> Issue:
        # check permissions for update issue
        if not self.permission_service.check_for_permission("change_issue"):
            raise PermissionDenied()

        fields = ["title", "description", "thumbnail", "status", "task"]

        issue, _ = model_update(
            instance=issue, fields=fields, data=data, user=self.user
        )
        return issue

    @transaction.atomic
    def delete(self, *, issue: Issue) -> None:
        # check permissions for delete issue
        if not self.permission_service.check_for_permission("delete_issue"):
            raise PermissionDenied()

        issue.delete()


# ------------------------------------------------------------------------------
# Comment Service
# ------------------------------------------------------------------------------


class CommentService:
    def __init__(self, user):
        self.user = user
        self.permission_service = AbstractPermissionService(user=user)

    @transaction.atomic
    def create(self, *, body: str, issue: Issue) -> Issue:
        # check permissions for add comment
        if not self.permission_service.check_for_permission("add_comment"):
            raise PermissionDenied()

        comment = Comment.objects.create(body=body, issue=issue)
        comment.full_clean()
        comment.save(user=self.user)

        return comment

    @transaction.atomic
    def update(self, *, comment: Comment, data: dict) -> Comment:
        # check permissions for update comment
        if not self.permission_service.check_for_permission("change_comment"):
            raise PermissionDenied()

        fields = ["body"]

        comment, _ = model_update(
            instance=comment, fields=fields, data=data, user=self.user
        )
        return comment

    @transaction.atomic
    def delete(self, *, comment: Comment) -> None:
        if not self.permission_service.check_for_permission("delete_comment"):
            raise PermissionDenied()

        comment.delete()
