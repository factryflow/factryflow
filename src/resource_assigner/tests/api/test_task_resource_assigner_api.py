# import json

# import pytest
# from factories import ResourceFactory, ResourcePoolFactory, TaskFactory
# from resource_assigner.models import TaskResourceAssigment


# @pytest.fixture
# def payload():
#     TaskFactory.create()
#     ResourcePoolFactory.create()
#     ResourceFactory.create_batch(2)
#     return {
#         "task_id": 1,
#         "resource_group_id": 1,
#         "resource_ids": [1, 2],
#         "resource_count": None,
#         "use_all_resources": False,
#         "is_direct": True,
#     }


# @pytest.mark.django_db
# def test_create_task_resource_assignment(api_client, payload):
#     response = api_client.post(
#         "/api/task-resource-assignments",
#         json.dumps(payload, default=str),
#         content_type="application/json",
#     )

#     print(response.json())
#     assert response.status_code == 201

#     instance = TaskResourceAssigment.objects.get(id=1)
#     assert instance.task.id == payload["task_id"]
#     assert instance.resource_group.id == payload["resource_group_id"]
#     assert instance.resources.count() == 2
#     assert instance.resource_count is None
#     assert instance.use_all_resources is False
#     assert instance.is_direct is True


# @pytest.mark.django_db
# def test_list_task_resource_assignment(api_client):

#     response = api_client.post(
#         "/api/task-resource-assignments",
#         json.dumps(payload, default=str),
#         content_type="application/json",
#     )

#     response = api_client.get("/api/task-resource-assignments")

#     assert response.status_code == 200
#     assert len(response.json()) == 1
