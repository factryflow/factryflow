import pytest
from django.contrib.auth.models import Permission

from users.models import User
from users.services import UserService

# @pytest.fixture
# def resource_data():
#     return {
#         "name": "Resource 1",
#         "external_id": "1",
#         "resource_type": ResourceTypeChoices.OPERATOR,
#         "users": UserFactory.create_batch(2),
#         "weekly_shift_template": WeeklyShiftTemplateFactory(),
#     }


# @pytest.mark.django_db
# def test_can_create_resource(resource_data):
#     user = UserFactory()

#     resource = ResourceService(user=user).create(**resource_data)

#     assert resource.name == resource_data["name"]
#     assert resource.external_id == resource_data["external_id"]
#     assert resource.users.count() == 2


@pytest.mark.django_db
def test_can_change_password():
    user = User.objects.create_user(username="testuser", password="12345")
    user.user_permissions.add(Permission.objects.get(codename="change_user"))
    user.save()
    user.refresh_from_db()

    user_service = UserService(user)

    user_service.change_password(data={"new_password": "new-password"})
    user.refresh_from_db()
    assert user.check_password("new-password") is True


# @pytest.mark.django_db
# def test_can_update_relationships(resource_data):
#     user = UserFactory()

#     resource = ResourceService(user=user).create(**resource_data)

#     new_weekly_shift_template = WeeklyShiftTemplateFactory()

#     updated_resource = ResourceService(user=user).update(
#         instance=resource,
#         data={
#             "weekly_shift_template": new_weekly_shift_template,
#         },
#     )

#     assert updated_resource.id == resource.id
#     assert updated_resource.weekly_shift_template == new_weekly_shift_template


# @pytest.mark.django_db
# def test_can_delete_resource(resource_data):
#     user = UserFactory()

#     resource = ResourceService(user=user).create(**resource_data)

#     ResourceService(user=user).delete(instance=resource)

#     assert Resource.objects.count() == 0
