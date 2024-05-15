from api.utils import CRUDModelViewSet
from ninja import Router

from resource_assigner.models import (
    AssigmentRule,
    AssignmentConstraint,
)
from resource_assigner.services import (
    AssigmentRuleService,
    AssignmentConstraintService,
)

from .schemas import (
    AssigmentRuleIn,
    AssigmentRuleOut,
    AssignmentConstraintIn,
    AssignmentConstraintOut,
)

# ------------------------------------------------------------------------------
# Resource Assigner API
# ------------------------------------------------------------------------------

resource_assigner_router = Router()

task_resource_assigment_viewset = CRUDModelViewSet(
    model=AssignmentConstraint,
    path="/task-resource-assignments",
    service=AssignmentConstraintService,
    input_schema=AssignmentConstraintIn,
    output_schema=AssignmentConstraintOut,
    tags=["Task Resource Assignments"],
)

task_resource_assigment_router = task_resource_assigment_viewset.router
resource_assigner_router.add_router("", task_resource_assigment_router)

# ------------------------------------------------------------------------------
# Assigment Rule API
# ------------------------------------------------------------------------------

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
