import factory
from common.utils.tests import faker
from resource_manager.models import Resource, ResourceGroup, ResourceTypeChoices

from .resource_calendar_factories import WeeklyShiftTemplateFactory
from .user_factories import UserFactory


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    resource_type = ResourceTypeChoices.OPERATOR
    external_id = ""
    notes = ""
    weekly_shift_template = factory.SubFactory(WeeklyShiftTemplateFactory)

    class Params:
        with_users = factory.Trait(
            users=factory.lazy_attribute(lambda _: UserFactory.create_batch(2))
        )


class ResourceGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceGroup

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    external_id = ""
    notes = ""
