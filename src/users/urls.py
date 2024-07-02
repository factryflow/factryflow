from django.urls import path

from users.views.change_password import ChangePasswordView
from users.views.detail_view import (
    USER_VIEWS,
)

urlpatterns = [
    # users urls
    path("users/new/", USER_VIEWS.show_model_form, name="users_form"),
    path("users/", USER_VIEWS.get_all_instances, name="users"),
    path(
        "users-create/",
        USER_VIEWS.create_or_update_model_instance,
        name="users_write",
    ),
    path(
        "users/delete/<int:id>/",
        USER_VIEWS.delete_obj_instance,
        name="delete_users",
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
]
