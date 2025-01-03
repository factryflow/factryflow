from http import HTTPStatus

from common.api import common_router
from django.core.exceptions import (
    FieldError,
    ObjectDoesNotExist,
    PermissionDenied,
    ValidationError,
)
from django.http import Http404
from job_manager.api.viewsets import job_manager_router
from microbatching.api import microbatch_router
from ninja import NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError
from ninja.security import APIKeyHeader
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja_jwt.routers.obtain import obtain_pair_router
from resource_assigner.api import resource_assigner_router

# import and register routers
from resource_calendar.api import resource_calendar_router
from resource_manager.api import resource_manager_router
from users.api import router as user_router
from users.models import User


class ApiKey(APIKeyHeader, JWTBaseAuthentication):
    def __init__(self, user_model):
        self.user_model = user_model
        super().__init__()

    param_name = "X-API-Key"

    def authenticate(self, request, key):
        return self.jwt_authenticate(request, token=key)


header_key = ApiKey(user_model=User)


api = NinjaAPI(
    title="Factryflow APIs",
    version="1.0.0",
    description=(
        """Factryflow API for managing resources, jobs, tasks, and more.
        This API provides endpoints to handle resource allocation, job scheduling, 
        user management, and various other functionalities essential for efficient 
        workflow management in a factoryflow.
        """
    ),
    docs_url="/docs",
    openapi_url="/openapi.json",
    auth=header_key,
)


api.add_router("/token", tags=["Auth"], router=obtain_pair_router)
api.add_router("", resource_manager_router)


api.add_router("", job_manager_router)
api.add_router("", resource_calendar_router)
api.add_router("", resource_assigner_router)
api.add_router("", user_router)
api.add_router("", common_router)
api.add_router("", microbatch_router)


@api.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc):
    return api.create_response(
        request,
        {"message": "ObjectDoesNotExist", "detail": str(exc)},
        status=HTTPStatus.NOT_FOUND,
    )


@api.exception_handler(Http404)
def handle_404_error(request, exc: Http404):
    return api.create_response(
        request,
        data={"message": "ObjectNotFound", "detail": str(exc)},
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
