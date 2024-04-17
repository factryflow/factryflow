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
    ResourcePoolFactory,
    WorkUnitFactory,
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
    external_id = ""
    notes = ""


class AssigmentConstraintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignmentConstraint

    task = None
    assignment_rule = None
    resource_pool = None
    required_units = 1
    is_direct = True

    class Params:
        with_task = factory.Trait(
            task=factory.SubFactory(TaskFactory),
        )
        with_assignment_rule = factory.Trait(
            assignment_rule=factory.SubFactory(AssigmentRuleFactory)
        )
        # with_resource_pool = factory.Trait(
        #     resource_pool=factory.lazy_attribute()
        # )
        with_resources = factory.Trait(
            resources=factory.lazy_attribute(lambda _: ResourceFactory.create_batch(2))
        )
        with_work_units = factory.Trait(
            work_units=factory.lazy_attribute(lambda _: WorkUnitFactory.create_batch(2))
        )


class TaskResourceAssigmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskResourceAssigment

    task = factory.SubFactory(TaskFactory)
    assigment_rule = factory.SubFactory(AssigmentRuleFactory)
    resource_pool = None
    resource_count = 1
    use_all_resources = False


    class Params:
        with_resource_pool = factory.Trait(
            resource_pool=factory.SubFactory(ResourcePoolFactory)
        )