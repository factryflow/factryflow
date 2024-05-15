from api.utils import CRUDModelViewSet
from ninja import Router

from common.models import CustomField
from common.services import CustomFieldService
from common.schemas import CustomFieldIn, CustomFieldOut


# customfield router

common_router = Router()

# ------------------------------------------------------------------------------
# CustomField APIs
# ------------------------------------------------------------------------------

custom_field_viewset = CRUDModelViewSet(
    model=CustomField,
    path="/custom-fields",
    service=CustomFieldService,
    input_schema=CustomFieldIn,
    output_schema=CustomFieldOut,
    tags=["Custom Fields"],
)

custom_field_router = custom_field_viewset.router
common_router.add_router("", custom_field_router)
