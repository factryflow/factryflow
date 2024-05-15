from enum import Enum
from ninja import Schema


class RoleChoices(str, Enum):
    Admin = "admin"
    Operator = "operator"
    Planner = "planner"
    ReadOnly = "read_only"


class RoleIn(Schema):
    user_id: int
    name: RoleChoices
