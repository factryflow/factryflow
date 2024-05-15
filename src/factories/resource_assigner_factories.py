import factory
from common.utils.tests import faker
from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
    Operator,
    TaskResourceAssigment,
)

from .job_manager_factories import TaskFactory, WorkCenterFactory
from .resource_manager_factories import (
    ResourceFactory,
    ResourceGroupFactory,
)


class AssigmentRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssigmentRule

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    external_id = ""
    description = ""
    notes = ""
    work_center = factory.SubFactory(WorkCenterFactory)
    is_active = True


class AssigmentRuleCriteriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssigmentRuleCriteria

    assigment_rule = factory.SubFactory(AssigmentRuleFactory)
    operator = Operator.EQUALS
    value = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    field = "name"


class AssigmentConstraintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignmentConstraint

    task = None
    assignment_rule = None
    resource_group = None
    is_direct = True

    class Params:
        with_task = factory.Trait(
            task=factory.SubFactory(TaskFactory),
        )
        with_assignment_rule = factory.Trait(
            assignment_rule=factory.SubFactory(AssigmentRuleFactory)
        )
        with_resource_group = factory.Trait(
            resource_group=factory.SubFactory(ResourceGroupFactory)
        )
        with_resources = factory.Trait(
            resources=factory.lazy_attribute(lambda _: ResourceFactory.create_batch(2))
        )


class TaskResourceAssigmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskResourceAssigment

    task = factory.SubFactory(TaskFactory)
    assigment_rule = factory.SubFactory(AssigmentRuleFactory)
    resource_count = 1
    use_all_resources = False

    class Params:
        with_resource_group = factory.Trait(
            resource_group=factory.lazy_attribute(
                lambda _: ResourceGroupFactory.create_batch(2)
            )
        )
