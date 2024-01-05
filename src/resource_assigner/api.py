from api.utils import CRUDModelViewSet
from ninja import Router

from resource_assigner.models import (
    AssigmentRule,
    TaskResourceAssigment,
)
from resource_assigner.services import (
    AssigmentRuleService,
    TaskResourceAssigmentService,
)

from .schemas import (
    AssigmentRuleIn,
    AssigmentRuleOut,
    TaskResourceAssigmentIn,
    TaskResourceAssigmentOut,
)

resource_assigner_router = Router()

task_resource_assigment_viewset = CRUDModelViewSet(
    model=TaskResourceAssigment,
    path="/task-resource-assignments",
    service=TaskResourceAssigmentService,
    input_schema=TaskResourceAssigmentIn,
    output_schema=TaskResourceAssigmentOut,
    tags=["Task Resource Assignments"],
)

task_resource_assigment_router = task_resource_assigment_viewset.router
resource_assigner_router.add_router("", task_resource_assigment_router)


assigment_rule_viewset = CRUDModelViewSet(
    model=AssigmentRule,
    path="/assigment-rules",
    service=AssigmentRuleService,
    input_schema=AssigmentRuleIn,
    output_schema=AssigmentRuleOut,
    tags=["Assigment Rules"],
)

assigment_rule_router = assigment_rule_viewset.router
resource_assigner_router.add_router("", assigment_rule_router)
