from datetime import timedelta

import factory
from common.utils.tests import faker


from .job_manager_factories import TaskFactory
from .resource_manager_factories import ResourceFactory
from scheduler.models import (
    SchedulerRuns,
    ResourceIntervals,
    ResourceAllocations,
    SchedulerStatusChoices,
)


class SchedulerRunsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchedulerRuns

    start_time = factory.lazy_attribute(lambda _: faker.future_datetime())
    end_time = factory.lazy_attribute(lambda _: faker.future_datetime())
    run_duration = factory.lazy_attribute(lambda _: timedelta(hours=1))

    status = SchedulerStatusChoices.STARTED
    details = "details description"

    class Params:
        with_notes = factory.Trait(notes=factory.lazy_attribute(lambda x: faker.text()))


class ResourceIntervalsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceIntervals

    run_id = factory.SubFactory(SchedulerRunsFactory)
    resource = factory.SubFactory(ResourceFactory)
    task = factory.SubFactory(TaskFactory)
    interval_start = factory.lazy_attribute(lambda _: faker.future_datetime())
    interval_end = factory.lazy_attribute(lambda _: faker.future_datetime())

    class Params:
        with_interval_start = factory.Trait(
            interval_start=factory.lazy_attribute(lambda x: faker.future_datetime())
        )
        with_interval_end = factory.Trait(
            interval_end=factory.lazy_attribute(lambda x: faker.future_datetime())
        )


class ResourceAllocationsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResourceAllocations

    run_id = factory.SubFactory(SchedulerRunsFactory)
    resource = factory.SubFactory(ResourceFactory)
    task = factory.SubFactory(TaskFactory)
