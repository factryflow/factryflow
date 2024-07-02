from django.urls import path

from .views import (
    USER_VIEWS,
)

urlpatterns = [
    # users urls
    path("users/new/", USER_VIEWS.show_model_form, name="users_form"),
    path("users/", USER_VIEWS.get_all_instances, name="users"),
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
]
