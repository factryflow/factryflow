from django.urls import path

from . import views

urlpatterns = [
    path("issues/new/", views.issues.show_issue_form, name="issue_form"),
    path("issue-create/", views.issues.save_issue_form, name="issue_create"),
    path("issues/", views.issues.show_issues_list, name="issue"),
    path("tag/<slug:tag_slug>/", views.issues.show_issues_list, name="issues_by_tag"),
    path(
        "issues/delete/<int:id>/",
        views.issues.request_issue_delete,
        name="delete_issue",
    ),
    path("issues/view/<int:id>/", views.issues.show_issue_form, name="view_issue"),
    path(
        "issues/view/<int:id>/edit=<str:edit>",
        views.issues.show_issue_form,
        name="edit_issue",
    ),
    path("issues/comment/<int:id>/", views.comments.post_comment, name="comments"),
]
