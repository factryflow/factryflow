from http import HTTPStatus

from ninja import Schema


class LoginSchema(Schema):
    username: str
    password: str


class DeleteResponseSchema(Schema):
    # Schema for DELETE response
    status: int = HTTPStatus.OK
    message: str
