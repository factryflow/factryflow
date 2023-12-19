import factory
from common.utils.tests import faker
from resource_manager.models import Resource, ResourceGroup

from .resource_calendar_factories import WeeklyShiftTemplateFactory


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    external_id = ""
    weekly_shift_template = factory.SubFactory(WeeklyShiftTemplateFactory)

    class Params:
        with_resource_groups = factory.Trait(
            resource_groups=factory.lazy_attribute(
                lambda _: ResourceGroupFactory.create_batch(2)
            )
        )


class ResourceGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceGroup

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    external_id = ""

    # class Params:
    #     with_resources = factory.Trait(
    #         resources=factory.lazy_attribute(lambda _: ResourceFactory.create_batch(2))
    #     )
