import pytest
from factories.user_factories import UserFactory
from rolepermissions.roles import assign_role

from users.models import User
from users.services import UserService


@pytest.fixture
def user_data():
    return {
        "username": "test-username",
        "password": "test-password",
        "first_name": "FirstName",
        "last_name": "LastName",
        "groups": [],
    }


@pytest.mark.django_db
def test_can_create_user(user_data):
    user = UserFactory()

    new_user = UserService(user=user).create(**user_data)

    assert new_user.username == user_data["username"]
    assert User.objects.count() == 2


@pytest.mark.django_db
def test_can_change_password():
    user = User.objects.create_user(username="testuser", password="12345")
    assign_role(user, "admin")
    user.save()
    user.refresh_from_db()

    user_service = UserService(user)

    user_service.change_password(data={"new_password": "new-password"})
    user.refresh_from_db()
    assert user.check_password("new-password") is True


@pytest.mark.django_db
def test_can_update_user(user_data):
    user = UserFactory()

    user_service = UserService(user)

    new_user = user_service.create(**user_data)

    user_service.update(
        new_user,
        data={
            "first_name": "first-name",
            "last_name": "last-name",
            "require_password_change": True,
        },
    )

    new_user.refresh_from_db()

    assert new_user.first_name == "first-name"
    assert new_user.last_name == "last-name"
    assert new_user.require_password_change is True
