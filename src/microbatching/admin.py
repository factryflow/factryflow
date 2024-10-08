from django.contrib import admin

from microbatching.models.microbatch_flow import MicrobatchFlow, MicrobatchFlowStep
from microbatching.models.microbatch_rule import MicrobatchRule, MicrobatchRuleCriteria

admin.site.register(MicrobatchRule)
admin.site.register(MicrobatchRuleCriteria)
admin.site.register(MicrobatchFlow)
admin.site.register(MicrobatchFlowStep)
