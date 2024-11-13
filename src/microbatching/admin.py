from django.contrib import admin

from microbatching.models.microbatch_flow import (
    MicrobatchFlow,
    MicrobatchTask,
    MicrobatchTaskFlow,
)
from microbatching.models.microbatch_rule import (
    MicrobatchRule,
    MicrobatchRuleCriteria,
    MicrobatchRuleTaskMatch,
)

admin.site.register(MicrobatchRule)
admin.site.register(MicrobatchRuleCriteria)
admin.site.register(MicrobatchFlow)
admin.site.register(MicrobatchTaskFlow)
admin.site.register(MicrobatchRuleTaskMatch)
admin.site.register(MicrobatchTask)
