import factory
from common.utils.tests import faker
from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    Operator,
    TaskResourceAssigment,
)

from .job_manager_factories import TaskFactory, WorkCenterFactory
from .resource_manager_factories import ResourceFactory, ResourcePoolFactory


class TaskResourceAssigmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskResourceAssigment

    task = factory.SubFactory(TaskFactory)
    resource_pool = factory.SubFactory(ResourcePoolFactory)
    resource_count = None
    use_all_resources = False
    is_direct = True

    class Params:
        with_resources = factory.Trait(
            resources=factory.lazy_attribute(lambda _: ResourceFactory.create_batch(2))
        )


class AssigmentRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssigmentRule

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    description = ""
    resource_pool = factory.SubFactory(ResourcePoolFactory)
    work_center = factory.SubFactory(WorkCenterFactory)
    is_active = True


class AssigmentRuleCriteriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssigmentRuleCriteria

    assigment_rule = factory.SubFactory(AssigmentRuleFactory)
    operator = Operator.EQUALS
    value = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    field = "name"
