from api.utils import CRUDModelViewSet

from resource_manager.models import Resource
from resource_manager.services import ResourceService

from .schemas import ResourceIn, ResourceOut

resource_viewset = CRUDModelViewSet(
    model=Resource,
    path="/resources",
    service=ResourceService,
    input_schema=ResourceIn,
    output_schema=ResourceOut,
    tags=["resource"],
)

resource_router = resource_viewset.router
