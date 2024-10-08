# from common.views import CRUDView, CustomTableView

# # Create your views here.
# from microbatching.forms.microbatch_rule import (
#     MicrobatchRuleCriteriaForm,
#     MicrobatchRuleForm,
# )
# from microbatching.models.microbatch_rule import (
#     MicrobatchRule,
#     MicrobatchRuleCriteria,
#     Operator,
# )
# from microbatching.services import (
#     MicrobatchRuleService,
# )
# from microbatching.utils import get_model_fields

# # ------------------------------------------------------------------------------
# # Microbatch Views
# # ------------------------------------------------------------------------------

# MICROBATCH_RULE_MODEL_FIELDS = [
#     "id",
#     "item_name",
#     "work_center",
#     "batch_size",
# ]
# MICROBATCH_RULE_TABLE_HEADERS = [
#     "ID",
#     "Item Name",
#     "Work Center",
#     "Batch Size",
# ]

# MICROBATCH_RULE_SEARCH_FIELDS = ["item_name", "work_center", "batch_size"]

# MICROBATCH_RULE_MODEL_RELATION_HEADERS = [
#     "RULE CRITERIA",
#     "HISTORY",
# ]

# MICROBATCH_RULE_MODEL_RELATION_FIELDS = {
#     "rule_criteria": {
#         "model": MicrobatchRuleCriteria,
#         "model_name": "microbatch_rule_criteria",
#         "related_name": "microbatch_rule",
#         "headers": ["ID", "field", "operator", "value"],
#         "fields": ["id", "field", "operator", "value"],
#         "select_fields": {
#             "field": dict(
#                 get_model_fields(
#                     "Task", "job_manager", ["item", "task_type", "job", "work_center"]
#                 )
#             ),
#             "operator": dict(Operator.choices),
#         },
#         "relationship_fields": "microbatch_rule",
#         "show_edit_actions": True,
#     },
#     "history": {
#         "model_name": "history",
#         "related_name": "history",
#         "headers": ["ID", "History Date", "History Type", "History User"],
#         "fields": ["history_id", "history_date", "history_type", "history_user"],
#         "show_edit_actions": False,
#     },
# }

# MICROBATCH_RULE_CRITERIA_FORMSET_FORM_FIELDS = ["field", "operator", "value"]

# MICROBATCH_RULE_CRITERIA_FORMSET_OPTIONS = [
#     MicrobatchRuleCriteria,
#     MicrobatchRuleCriteriaForm,
#     "criteria",
#     MICROBATCH_RULE_CRITERIA_FORMSET_FORM_FIELDS,
#     "microbatch_rule_criteria",
# ]

# MICROBATCH_RULE_TABLE_VIEW = CustomTableView(
#     model=MicrobatchRule,
#     model_name="microbatch_rule",
#     fields=MICROBATCH_RULE_MODEL_FIELDS,
#     headers=MICROBATCH_RULE_TABLE_HEADERS,
#     model_relation_headers=MICROBATCH_RULE_MODEL_RELATION_HEADERS,
#     model_relation_fields=MICROBATCH_RULE_MODEL_RELATION_FIELDS,
#     search_fields_list=MICROBATCH_RULE_SEARCH_FIELDS,
# )

# MICROBATCH_RULE_VIEWS = CRUDView(
#     model=MicrobatchRule,
#     model_name="microbatch_rules",
#     model_service=MicrobatchRuleService,
#     model_form=MicrobatchRuleForm,
#     model_table_view=MICROBATCH_RULE_TABLE_VIEW,
#     formset_options=MICROBATCH_RULE_CRITERIA_FORMSET_OPTIONS,
# )
