from datetime import timedelta

import factory
from common.utils.tests import faker
from job_manager.models import (
    Dependency,
    DependencyType,
    Job,
    JobType,
    Task,
    TaskType,
    WorkCenter,
)


class JobTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobType

    name = factory.lazy_attribute(lambda _: faker.unique.word())
    external_id = ""
    notes = ""



class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    description = ""
    customer = ""
    external_id = ""
    notes = ""
    due_date = factory.lazy_attribute(lambda _: faker.date_this_year())
    priority = None
    planned_start_datetime = None
    planned_end_datetime = None
    job_status = "NP"  # Not Planned
    job_type = factory.SubFactory(JobTypeFactory)

    class Params:
        with_customer = factory.Trait(
            customer=factory.lazy_attribute(lambda x: faker.customer())
        )
        with_description = factory.Trait(
            description=factory.lazy_attribute(lambda x: faker.text())
        )
        with_priority = factory.Trait(priority=factory.lazy_attribute(lambda _: 1))
        planned = factory.Trait(
            planned_start_datetime=factory.lazy_attribute(
                lambda x: faker.future_datetime()
            ),
            planned_end_datetime=factory.lazy_attribute(
                lambda x: x.planned_start_datetime + timedelta(hours=10)
            ),
        )


class DependencyTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DependencyType

    name = factory.lazy_attribute(lambda _: faker.unique.word())
    external_id = ""
    notes = ""


class DependencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dependency

    name = factory.lazy_attribute(lambda x: faker.name())
    dependency_status = "PD"  # Pending
    dependency_type = factory.SubFactory(DependencyTypeFactory)
    external_id = ""
    notes = ""


class TaskTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskType

    name = factory.lazy_attribute(lambda _: faker.unique.word())
    external_id = ""
    notes = ""


class WorkCenterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkCenter

    name = factory.lazy_attribute(lambda _: faker.unique.word())
    external_id = ""
    notes = ""


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.lazy_attribute(lambda _: faker.unique.word())
    task_status = "NS"  # Not Started
    task_type = factory.SubFactory(TaskTypeFactory)
    work_center = factory.SubFactory(WorkCenterFactory)
    quantity = 1
    setup_time = 0
    teardown_time = 0
    run_time_per_unit = 1
    job = None
    external_id = ""
    notes = ""

    class Params:
        with_job = factory.Trait(job=factory.SubFactory(JobFactory))
