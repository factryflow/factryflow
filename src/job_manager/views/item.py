# views.py
from common.views import CRUDView, CustomTableView

from job_manager.forms import (
    ItemForm,
)
from job_manager.models import (
    Item,
)
from job_manager.services import (
    ItemService,
)


# ------------------------------------------------------------------------------
# Item Views
# ------------------------------------------------------------------------------

ITEM_MODEL_FIELDS = ["id", "name", "description", "notes"]

ITEM_SEARCH_FIELDS = ["name", "description", "notes", "id"]

ITEM_MODEL_RELATION_HEADERS = ["HISTORY"]
ITEM_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": ["ID", "Name", "User", "Notes", "History Date"],
        "fields": ["history_id", "name", "history_user", "notes", "history_date"],
        "show_edit_actions": False,
    },
}

ITEM_TABLE_VIEW = CustomTableView(
    model=Item,
    model_name="item",
    fields=ITEM_MODEL_FIELDS,
    model_relation_headers=ITEM_MODEL_RELATION_HEADERS,
    model_relation_fields=ITEM_MODEL_RELATION_FIELDS,
    search_fields_list=ITEM_SEARCH_FIELDS,
)

ITEM_VIEWS = CRUDView(
    model=Item,
    model_name="items",
    model_service=ItemService,
    model_form=ItemForm,
    model_table_view=ITEM_TABLE_VIEW,
)
