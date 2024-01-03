import factory
from common.utils.tests import faker
from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    Operator,
    TaskResourceAssigment,
)

from .job_manager_factories import TaskFactory, WorkCenterFactory
from .resource_manager_factories import ResourceGroupFactory


class TaskResourceAssigmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskResourceAssigment

    task = factory.SubFactory(TaskFactory)
    resource_group = factory.SubFactory(ResourceGroupFactory)
    # resources = factory.lazy_attribute(lambda _: ResourceFactory.create_batch(2))
    resource_count = None
    use_all_resources = False
    is_direct = False

    @factory.post_generation
    def resources(self, create, extracted, **kwargs):
        if not create:
            # If not creating TaskResourceAssigment instance, do nothing
            return

        if extracted:
            # If resources were provided, add them to the many-to-many relationship
            for resource in extracted:
                self.resources.set(resource)


class AssigmentRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssigmentRule

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    description = ""
    resource_group = factory.SubFactory(ResourceGroupFactory)
    work_center = factory.SubFactory(WorkCenterFactory)
    is_active = True


class AssigmentRuleCriteriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssigmentRuleCriteria

    assigment_rule = factory.SubFactory(AssigmentRuleFactory)
    operator = Operator.EQUALS
    value = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    field = "name"
