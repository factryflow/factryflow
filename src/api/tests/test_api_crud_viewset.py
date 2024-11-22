from django.test import TestCase
from ninja import NinjaAPI, Router
from job_manager.models import Task
from job_manager.schemas import TaskIn, TaskOut
from job_manager.services import TaskService
from api.utils import CRUDModelViewSet


def setup_ninja_api_with_router():
    """
    Sets up the NinjaAPI instance with CRUDModelViewSet for the Task model
    and registers it under the `/test` route for testing purposes.

    Returns:
        NinjaAPI: Initialized NinjaAPI instance with CRUD routes.
    """
    client = NinjaAPI()
    test_task_router = Router()

    viewset = CRUDModelViewSet(
        model=Task,
        service=TaskService,
        input_schema=TaskIn,
        output_schema=TaskOut,
        path="/tasks",
    )

    # Add the CRUDModelViewSet to the router and the router to the client
    test_task_router.add_router("", viewset.router)
    client.add_router("/test", test_task_router)

    return client


def extract_endpoint_details(api_client):
    """
    Extracts all endpoint details from the OpenAPI schema of the given NinjaAPI instance.

    Args:
        api_client (NinjaAPI): The NinjaAPI instance to extract endpoint details from.

    Returns:
        dict: A dictionary containing endpoint details mapped by HTTP method names.
    """
    data = api_client.get_openapi_schema()
    endpoints = {}

    for path, methods in data.get("paths", {}).items():
        for method, details in methods.items():
            method_name = (
                "LIST" if method == "get" and "id" not in path else method.upper()
            )
            if method in ["post", "get", "put", "delete"]:
                endpoint_details = {
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get("summary", ""),
                    "operationId": details.get("operationId", ""),
                    "parameters": details.get("parameters", []),
                }

            endpoints[method_name] = endpoint_details

    return endpoints


class TestCreateRoute(TestCase):
    # test case for the CREATE route of the CRUDModelViewSet
    def test_create_route(self):
        api_client = setup_ninja_api_with_router()
        all_details = extract_endpoint_details(api_client)

        # Verify CREATE route
        create_route = all_details["POST"]
        self.assertEqual(create_route["path"], "/api/test/tasks")
        self.assertEqual(create_route["method"], "POST")
        self.assertEqual(create_route["operationId"], "task_create")


class TestListRoute(TestCase):
    # test case for the LIST route of the CRUDModelViewSet
    def test_list_route(self):
        api_client = setup_ninja_api_with_router()
        all_details = extract_endpoint_details(api_client)

        # Verify LIST route
        list_route = all_details["LIST"]
        self.assertEqual(list_route["path"], "/api/test/tasks")
        self.assertEqual(list_route["method"], "GET")
        self.assertEqual(list_route["operationId"], "task_list")


class TestRetrieveRoute(TestCase):
    # test case for the RETRIEVE route of the CRUDModelViewSet
    def test_retrieve_route(self):
        api_client = setup_ninja_api_with_router()
        all_details = extract_endpoint_details(api_client)

        # Verify GET route
        get_route = all_details["GET"]
        self.assertEqual(get_route["path"], "/api/test/tasks/{id}")
        self.assertEqual(get_route["method"], "GET")
        self.assertEqual(get_route["operationId"], "task_retrieve")


class TestUpdateRoute(TestCase):
    # test case for the UPDATE route of the CRUDModelViewSet
    def test_update_route(self):
        api_client = setup_ninja_api_with_router()
        all_details = extract_endpoint_details(api_client)

        # Verify UPDATE route
        update_route = all_details["PUT"]
        self.assertEqual(update_route["path"], "/api/test/tasks/{id}")
        self.assertEqual(update_route["method"], "PUT")
        self.assertEqual(update_route["operationId"], "task_update")


class TestDeleteRoute(TestCase):
    # test case for the DELETE route of the CRUDModelViewSet
    def test_delete_route(self):
        api_client = setup_ninja_api_with_router()
        all_details = extract_endpoint_details(api_client)

        # Verify DELETE route
        delete_route = all_details["DELETE"]
        self.assertEqual(delete_route["path"], "/api/test/tasks/{id}")
        self.assertEqual(delete_route["method"], "DELETE")
        self.assertEqual(delete_route["operationId"], "task_delete")
