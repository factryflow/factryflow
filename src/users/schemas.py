from enum import Enum
from ninja import Schema

class RoleChoice(str, Enum):
    admin = "admin"
    operator = "operator"
    planner = "planner"
    read_only = "read_only"
    

class RoleIn(Schema):
    user_id: int
    name: RoleChoice