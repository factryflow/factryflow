from enum import Enum


class RoleChoices(str, Enum):
    """User role choices."""
    Admin = "admin"
    Operator = "operator"
    Planner = "planner"
    ReadOnly = "read_only"
