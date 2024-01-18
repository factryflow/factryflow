from api.utils import CRUDModelViewSet
from ninja import Router

from resource_manager.models import Resource, ResourcePool, WorkUnit
from resource_manager.services import (
    ResourcePoolService,
    ResourceService,
    WorkUnitService,
)

from .schemas import (
    ResourceIn,
    ResourceOut,
    ResourcePoolIn,
    ResourcePoolOut,
    WorkUnitIn,
    WorkUnitOut,
)

resource_manager_router = Router()

resource_viewset = CRUDModelViewSet(
    model=Resource,
    path="/resources",
    service=ResourceService,
    input_schema=ResourceIn,
    output_schema=ResourceOut,
    tags=["Resources"],
)

resource_router = resource_viewset.router
resource_manager_router.add_router("", resource_router)

work_unit_viewset = CRUDModelViewSet(
    model=WorkUnit,
    path="/work-units",
    service=WorkUnitService,
    input_schema=WorkUnitIn,
    output_schema=WorkUnitOut,
    tags=["Work Units"],
)

work_unit_router = work_unit_viewset.router
resource_manager_router.add_router("", work_unit_router)

resource_pool_viewset = CRUDModelViewSet(
    model=ResourcePool,
    path="/resource-pools",
    service=ResourcePoolService,
    input_schema=ResourcePoolIn,
    output_schema=ResourcePoolOut,
    tags=["Resource Pools"],
)

resource_pool_router = resource_pool_viewset.router
resource_manager_router.add_router("", resource_pool_router)
