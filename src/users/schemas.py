from ninja import Schema
from users.enums import RoleChoices


class RoleIn(Schema):
    user_id: int
    name: RoleChoices
