import factory
from common.utils.tests import faker
from resource_manager.models import Resource, ResourcePool, WorkUnit

from .resource_calendar_factories import WeeklyShiftTemplateFactory
from .user_factories import UserFactory


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    resource_type = "O"
    external_id = ""
    notes = ""
    weekly_shift_template = factory.SubFactory(WeeklyShiftTemplateFactory)

    class Params:
        with_resource_pools = factory.Trait(
            resource_pools=factory.lazy_attribute(
                lambda _: ResourcePoolFactory.create_batch(2)
            )
        )
        with_work_units = factory.Trait(
            work_units=factory.lazy_attribute(lambda _: WorkUnitFactory.create_batch(2))
        )
        with_users = factory.Trait(
            users=factory.lazy_attribute(lambda _: UserFactory.create_batch(2))
        )


class ResourcePoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourcePool

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    external_id = ""
    notes = ""


class WorkUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkUnit

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    external_id = ""
    notes = ""
