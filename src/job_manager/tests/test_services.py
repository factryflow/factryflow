import pytest
from factories.job_manager_factories import JobStatusFactory, JobTypeFactory
from job_manager.services import job_create_or_update, job_type_create


@pytest.mark.django_db
def test_create_job_type():
    job_type = job_type_create(name="test")

    assert job_type.name == "test"
    assert job_type.id is not None
    assert job_type.id > 0


@pytest.mark.django_db
def test_job_create():
    job_type = JobTypeFactory()
    job_status = JobStatusFactory()

    job_data = {
        "name": "test",
        "due_date": "2021-01-01",
        "priority": 1,
    }

    job = job_create_or_update(
        job_data=job_data, job_type=job_type, job_status=job_status
    )

    assert job.name == "test"
    assert job.id is not None
