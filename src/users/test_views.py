# Create your views here.
from common.views import CRUDView, CustomTableView

from users.forms import UserForm
from users.models import User
from users.services import UserService

# ------------------------------------------------------------------------------
# User VIEWS
# ------------------------------------------------------------------------------


USER_MODEL_FIELDS = [
    "id",
    "email",
    "first_name",
    "last_name",
]

USER_SEARCH_FIELDS = ["email", "first_name", "last_name"]
USER_TABLE_HEADERS = [
    "ID",
    "E-mail",
    "First Name",
    "Last Name",
]

# USER_MODEL_RELATION_HEADERS = ["HISTORY"]
# USER_MODEL_RELATION_FIELDS = {
#     "history": [
#         "history",
#         ["ID", "History Date", "History Type", "History User"],
#         ["id", "history_date", "history_type", "history_user"],
#     ],
# }

UserTableView = CustomTableView(
    model=User,
    model_name="user",
    fields=USER_MODEL_FIELDS,
    headers=USER_TABLE_HEADERS,
    # model_relation_headers=USER_MODEL_RELATION_HEADERS,
    # model_relation_fields=USER_MODEL_RELATION_FIELDS,
    # status_filter_field=USER_STATUS_FILTER_FIELD,
    search_fields_list=USER_SEARCH_FIELDS,
)

USER_VIEWS = CRUDView(
    model=User,
    model_name="user",
    model_service=UserService,
    model_form=UserForm,
    model_table_view=UserTableView,
)
