from api.utils import CRUDModelViewSet
from ninja import Router

from resource_manager.models import Resource, ResourceGroup
from resource_manager.services import (
    ResourceGroupService,
    ResourceService,
)

from resource_manager.schemas import (
    ResourceIn,
    ResourceOut,
    ResourceGroupIn,
    ResourceGroupOut,
)

# ------------------------------------------------------------------------------
# Resource Manager API
# ------------------------------------------------------------------------------

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


# ------------------------------------------------------------------------------
# Resource Group API
# ------------------------------------------------------------------------------

resource_group_viewset = CRUDModelViewSet(
    model=ResourceGroup,
    path="/resource-groups",
    service=ResourceGroupService,
    input_schema=ResourceGroupIn,
    output_schema=ResourceGroupOut,
    tags=["Resource Groups"],
)

resource_group_router = resource_group_viewset.router
resource_manager_router.add_router("", resource_group_router)
