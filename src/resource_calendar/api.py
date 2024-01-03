from api.utils import CRUDModelViewSet
from ninja import Router

from resource_calendar.models import (
    OperationalException,
    OperationalExceptionType,
    WeeklyShiftTemplate,
    WeeklyShiftTemplateDetail,
)
from resource_calendar.services import (
    OperationalExceptionService,
    OperationalExceptionTypeService,
    WeeklyShiftTemplateDetailService,
    WeeklyShiftTemplateService,
)

from .schemas import (
    OperationalExceptionIn,
    OperationalExceptionOut,
    OperationalExceptionTypeIn,
    OperationalExceptionTypeOut,
    WeeklyShiftTemplateDetailIn,
    WeeklyShiftTemplateDetailOut,
    WeeklyShiftTemplateIn,
    WeeklyShiftTemplateOut,
)

resource_calendar_router = Router()

weekly_shift_template_viewset = CRUDModelViewSet(
    model=WeeklyShiftTemplate,
    path="/weekly-shift-templates",
    service=WeeklyShiftTemplateService,
    input_schema=WeeklyShiftTemplateIn,
    output_schema=WeeklyShiftTemplateOut,
    tags=["Weekly Shift Templates"],
)

weekly_shift_template_router = weekly_shift_template_viewset.router
resource_calendar_router.add_router("", weekly_shift_template_router)


weekly_shift_template_detail_viewset = CRUDModelViewSet(
    model=WeeklyShiftTemplateDetail,
    path="/weekly-shift-template-details",
    service=WeeklyShiftTemplateDetailService,
    input_schema=WeeklyShiftTemplateDetailIn,
    output_schema=WeeklyShiftTemplateDetailOut,
    tags=["Weekly Shift Template Details"],
)

weekly_shift_template_detail_router = weekly_shift_template_detail_viewset.router
resource_calendar_router.add_router("", weekly_shift_template_detail_router)


operational_exception_type_viewset = CRUDModelViewSet(
    model=OperationalExceptionType,
    path="/operational-exception-types",
    service=OperationalExceptionTypeService,
    input_schema=OperationalExceptionTypeIn,
    output_schema=OperationalExceptionTypeOut,
    tags=["Operational Exception Types"],
)

operational_exception_type_router = operational_exception_type_viewset.router
resource_calendar_router.add_router("", operational_exception_type_router)


operational_exception_viewset = CRUDModelViewSet(
    model=OperationalException,
    path="/operational-exceptions",
    service=OperationalExceptionService,
    input_schema=OperationalExceptionIn,
    output_schema=OperationalExceptionOut,
    tags=["Operational Exceptions"],
)

operational_exception_router = operational_exception_viewset.router
resource_calendar_router.add_router("", operational_exception_router)
