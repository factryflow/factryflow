import factory
from common.utils.tests import faker
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.lazy_attribute(lambda _: faker.unique.user_name())
    email = factory.lazy_attribute(lambda _: faker.unique.email())
    password = factory.lazy_attribute(lambda _: faker.password())
    first_name = factory.lazy_attribute(lambda _: faker.first_name())
    last_name = factory.lazy_attribute(lambda _: faker.last_name())
    is_active = True
    is_staff = False
    is_superuser = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = super()._create(model_class, *args, **kwargs)
        assign_role(user, "admin")  # Assign "admin" role to the created user
        return user
