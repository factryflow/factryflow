from api.utils import CRUDModelViewSet
from ninja import Router

from microbatching.models.microbatch_flow import MicrobatchFlow
from microbatching.services.microbatch_flow import MicrobatchFlowService
from microbatching.schemas.microbatch_flow import MicrobatchFlowIn, MicrobatchFlowOut

# define router
microbatch_router = Router()


# ------------------------------------------------------------------------------
# MicrobatchFlow APIs
# ------------------------------------------------------------------------------

microbatch_flow_viewset = CRUDModelViewSet(
    model=MicrobatchFlow,
    path="/microbatch-flows",
    service=MicrobatchFlowService,
    input_schema=MicrobatchFlowIn,
    output_schema=MicrobatchFlowOut,
    tags=["Microbatch Flows"],
)

microbatch_router.add_router("", microbatch_flow_viewset.router)
