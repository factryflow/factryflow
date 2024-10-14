from .crud_view import CRUDView
from .table_view import CustomTableView

from common.forms import CustomFieldForm
from common.models import CustomField, FieldType
from common.services import CustomFieldService

# ------------------------------------------------------------------------------
# Custom Field Views
# ------------------------------------------------------------------------------

CUSTOM_FIELD_MODEL_FIELDS = [
    "id",
    "name",
    "label",
    "content_type",
    "field_type",
    "is_required",
    "description",
]
CUSTOM_FIELD_TABLE_HEADERS = [
    "ID",
    "Field Name",
    "Label",
    "Content Type",
    "Field Type",
    "Is Required",
    "Description",
]

CUSTOM_FIELD_SEARCH_FIELDS = ["name", "field_type", "label", "description"]


CUSTOM_FIELD_STATUS_FILTER_FIELD = "field_type"

CUSTOM_FIELD_MODEL_RELATION_HEADERS = ["HISTORY"]
CUSTOM_FIELD_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": [
            "ID",
            "Name",
            "User",
            "Label",
            "Type",
            "Description",
            "History Date",
        ],
        "fields": [
            "history_id",
            "name",
            "history_user",
            "label",
            "field_type",
            "description",
            "history_date",
        ],
    },
}


CustomFieldTableView = CustomTableView(
    model=CustomField,
    model_name="custom_field",
    fields=CUSTOM_FIELD_MODEL_FIELDS,
    headers=CUSTOM_FIELD_TABLE_HEADERS,
    model_relation_headers=CUSTOM_FIELD_MODEL_RELATION_HEADERS,
    model_relation_fields=CUSTOM_FIELD_MODEL_RELATION_FIELDS,
    status_filter_field=CUSTOM_FIELD_STATUS_FILTER_FIELD,
    status_choices_class=FieldType,
    search_fields_list=CUSTOM_FIELD_SEARCH_FIELDS,
)

CUSTOM_FIELD_VIEWS = CRUDView(
    model=CustomField,
    model_name="custom_fields",
    model_service=CustomFieldService,
    model_form=CustomFieldForm,
    model_table_view=CustomFieldTableView,
)
