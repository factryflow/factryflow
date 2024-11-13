from api.utils import CRUDModelViewSet
from microbatching.api.microbatch_flow import microbatch_router

from microbatching.models.microbatch_rule import (
    MicrobatchRule,
    MicrobatchRuleCriteria,
)
from microbatching.services.microbatch_rule import (
    MicrobatchRuleService,
    MicrobatchRuleCriteriaService,
)
from microbatching.schemas.microbatch_rule import (
    MicrobatchRuleIn,
    MicrobatchRuleOut,
    MicrobatchRuleCriteriaIn,
    MicrobatchRuleCriteriaOut,
)


# ------------------------------------------------------------------------------
# MicrobatchRuleCriteria APIs
# ------------------------------------------------------------------------------

microbatch_rule_criteria_viewset = CRUDModelViewSet(
    model=MicrobatchRuleCriteria,
    path="/microbatch-rule-criteria",
    service=MicrobatchRuleCriteriaService,
    input_schema=MicrobatchRuleCriteriaIn,
    output_schema=MicrobatchRuleCriteriaOut,
    tags=["Microbatch Rule Criteria"],
)

microbatch_router.add_router("", microbatch_rule_criteria_viewset.router)


# ------------------------------------------------------------------------------
# MicrobatchRule APIs
# ------------------------------------------------------------------------------

microbatch_rule_viewset = CRUDModelViewSet(
    model=MicrobatchRule,
    path="/microbatch-rules",
    service=MicrobatchRuleService,
    input_schema=MicrobatchRuleIn,
    output_schema=MicrobatchRuleOut,
    tags=["Microbatch Rules"],
)

microbatch_router.add_router("", microbatch_rule_viewset.router)
