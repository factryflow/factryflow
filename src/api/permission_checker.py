from rolepermissions.checkers import has_permission
from http import HTTPStatus
from ninja import HTTPError

# write a decorator to get operations id and user and check if user has permission to access that operation
# if user has permission then return the function else raise 403 error
def has_permission_decorator(operation_id):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if has_permission(request.user, operation_id):
                return func(request, *args, **kwargs)
            else:
                raise HTTPError(HTTPStatus.FORBIDDEN, "You don't have permission to access this operation")
        return wrapper
    return decorator