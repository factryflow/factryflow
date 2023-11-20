from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    # path("register/", views.Logout.as_view(), name="register"),
]
