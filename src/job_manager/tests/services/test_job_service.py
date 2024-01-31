import pytest
from factories import UserFactory
from factories.job_manager_factories import JobFactory, JobTypeFactory
from job_manager.models import Job, JobStatusChoices
from job_manager.services import JobService


@pytest.mark.django_db
def test_job_create():
    job_type = JobTypeFactory()
    user = UserFactory()

    job_data = {
        "name": "test",
        "due_date": "2021-01-01",
        "priority": 1,
        "job_status": JobStatusChoices.NOT_PLANNED.value,
        "job_type": job_type,
    }

    job = JobService(user=user).create(**job_data)

    assert job.name == "test"
    assert job.id is not None
    assert job.description == ""
    assert job.priority == 1


@pytest.mark.django_db
def test_job_update():
    job = JobFactory(name="test")
    user = UserFactory()

    data = {
        "name": "update_name",
    }
    job = JobService(user=user).update(job=job, data=data)

    assert job.name == "update_name"
    assert job.id is not None
    assert job.job_status == "NP"


@pytest.mark.django_db
def test_job_delete():
    job = JobFactory(name="test")
    user = UserFactory()

    JobService(user=user).delete(job=job)

    assert Job.objects.count() == 0


@pytest.mark.django_db
def test_job_update_priority():
    job_1 = JobFactory(name="test")
    job_2 = JobFactory(name="test")

    assert job_1.priority == 0
    assert job_2.priority == 1

    job_2.update_priority(0)

    job_2.refresh_from_db()
    job_1.refresh_from_db()

    assert job_1.priority == 1
    assert job_2.priority == 0
