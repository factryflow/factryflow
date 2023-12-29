from api.utils import CRUDModelViewSet
from ninja import Router

from job_manager.models import Dependency, DependencyType, Job, JobType, Task, TaskType
from job_manager.services import (
    DependencyService,
    DependencyTypeService,
    JobService,
    JobTypeService,
    TaskService,
    TaskTypeService,
)

from schemas import (
    DependencyIn,
    DependencyOut,
    DependencyTypeIn,
    DependencyTypeOut,
    JobIn,
    JobOut,
    JobTypeIn,
    JobTypeOut,
    TaskIn,
    TaskOut,
    TaskTypeIn,
    TaskTypeOut,
)

# job manager router
job_manager_router = Router()


dependency_type_viewset = CRUDModelViewSet(
    model=DependencyType,
    path="/dependency-types",
    service=DependencyTypeService,
    input_schema=DependencyTypeIn,
    output_schema=DependencyTypeOut,
    tags=["Dependency Types"],
)


dependency_type_router = dependency_type_viewset.router
job_manager_router.add_router("", dependency_type_router)


dependency_viewset = CRUDModelViewSet(
    model=Dependency,
    path="/dependencies",
    service=DependencyService,
    input_schema=DependencyIn,
    output_schema=DependencyOut,
    tags=["Dependencies"],
)

dependency_router = dependency_viewset.router
job_manager_router.add_router("", dependency_router)


job_type_viewset = CRUDModelViewSet(
    model=JobType,
    path="/job-types",
    service=JobTypeService,
    input_schema=JobTypeIn,
    output_schema=JobTypeOut,
    tags=["Job Types"],
)

job_type_router = job_type_viewset.router
job_manager_router.add_router("", job_type_router)


job_viewset = CRUDModelViewSet(
    model=Job,
    path="/jobs",
    service=JobService,
    input_schema=JobIn,
    output_schema=JobOut,
    tags=["Jobs"],
)

job_router = job_viewset.router
job_manager_router.add_router("", job_router)


task_type_viewset = CRUDModelViewSet(
    model=TaskType,
    path="/task-types",
    service=TaskTypeService,
    input_schema=TaskTypeIn,
    output_schema=TaskTypeOut,
    tags=["Task Types"],
)

task_type_router = task_type_viewset.router
job_manager_router.add_router("", task_type_router)


task_viewset = CRUDModelViewSet(
    model=Task,
    path="/tasks",
    service=TaskService,
    input_schema=TaskIn,
    output_schema=TaskOut,
    tags=["Tasks"],
)

task_router = task_viewset.router
job_manager_router.add_router("", task_router)
