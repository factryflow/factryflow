from http import HTTPStatus

from django.core.exceptions import (
    FieldError,
    ObjectDoesNotExist,
    PermissionDenied,
    ValidationError,
)
from ninja import NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError
from ninja.security import APIKeyHeader


# import and register routers
from resource_calendar.api import resource_calendar_router
from resource_assigner.api import resource_assigner_router
from resource_manager.api import resource_manager_router
from job_manager.api import job_manager_router

class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        # TODO add api key to env file
        if key == "supersecret":
            return key


header_key = ApiKey()

api = NinjaAPI(auth=header_key)

api.add_router("", resource_manager_router)


api.add_router("", job_manager_router)
api.add_router("", resource_calendar_router)
api.add_router("", resource_assigner_router)


@api.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc):
    return api.create_response(
        request,
        {"message": "ObjectDoesNotExist", "detail": str(exc)},
        status=HTTPStatus.NOT_FOUND,
    )


@api.exception_handler(PermissionDenied)
def handle_permission_error(request, exc: PermissionDenied):
    return api.create_response(
        request,
        {
            "message": "PermissionDenied",
            "detail": "You don't have the permission to access this resource.",
        },
        status=HTTPStatus.FORBIDDEN,
    )


@api.exception_handler(NinjaValidationError)
def handle_ninja_validation_error(request, exc: NinjaValidationError):
    mapped_msg = {error["loc"][-1]: error["msg"] for error in exc.errors}
    return api.create_response(
        request,
        data={"message": "NinjaValidationError", "detail": mapped_msg},
        status=HTTPStatus.BAD_REQUEST,
    )


@api.exception_handler(ValidationError)
def handle_validation_error(request, exc: ValidationError):
    status = HTTPStatus.BAD_REQUEST
    for field, errors in exc.error_dict.items():
        for error in errors:
            if error.code in ["unique", "unique_together"]:
                status = HTTPStatus.CONFLICT
    return api.create_response(
        request,
        data={"message": "ValidationError", "detail": exc.message_dict},
        status=status,
    )


@api.exception_handler(FieldError)
def handle_field_error(request, exc: FieldError):
    return api.create_response(
        request,
        data={"message": "FieldError", "detail": str(exc)},
        status=HTTPStatus.BAD_REQUEST,
    )
