from django.urls import path

from users.views.admin_change_password import AdminChangePasswordView
from users.views.change_password import ChangePasswordView
from users.views.detail_view import (
    USER_VIEWS,
)

app_name = "users"

urlpatterns = [
    # users urls
    path("users/new/", USER_VIEWS.show_model_form, name="users_form"),
    path("users/", USER_VIEWS.get_all_instances, name="list"),
    path(
        "users/write/",
        USER_VIEWS.create_or_update_model_instance,
        name="users_write",
    ),
    path("users/view/<int:id>/", USER_VIEWS.show_model_form, name="view_users"),
    path(
        "users/view/<int:id>/edit=<str:edit>",
        USER_VIEWS.show_model_form,
        name="edit_users",
    ),
    path(
        "users/change-password/", ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "users/change-password/<int:id>",
        AdminChangePasswordView.as_view(),
        name="admin_change_password",
    ),
]
