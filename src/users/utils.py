from http import HTTPStatus

from django.contrib.auth.models import Permission
from functools import wraps

def get_all_permissions():
    # to get all permissions from django.contrib.auth.models.Permission
    permissions = set()
    for permission in Permission.objects.all():
        permissions.add(permission.codename)
    return permissions




def get_all_api_operations_id_from_urlpatterns():
    from api.api import api
    # to get all api operations id from urlpatterns
    method_names = set()

    api_openapi_schema = api.get_openapi_schema()
    unusable_function_names = [
        "api-root",
        "get",
        "create",
        "update",
        "delete",
        "list",
        "openapi-json",
        "openapi-view",
    ]

    try:
        # get operation_id from api
        for path in api_openapi_schema["paths"]:
            # to get all method in path
            for method in api_openapi_schema["paths"][path]:
                operation_id = api_openapi_schema["paths"][path][method]["operationId"]

                # check if operation_id is not in function_names and unusable_function_names
                if (
                    operation_id not in method_names
                    and operation_id not in unusable_function_names
                ):
                    method_names.add(operation_id)

        return method_names
    except Exception as e:
        print(e)


# decorator to check if user is superuser or not
def is_superuser(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return {
                "message": "PermissionDenied", "detail": "User is not superuser",
                "status":HTTPStatus.FORBIDDEN,
            }

    return wrapper