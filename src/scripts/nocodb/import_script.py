import datetime
import json

from job_manager.models import Job, JobType, WorkCenter
from job_manager.models.item import Item
from job_manager.models.task import Task
from resource_assigner.models import (
    AssigmentRule,
    AssigmentRuleCriteria,
    AssignmentConstraint,
)
from resource_calendar.models import WeeklyShiftTemplate, WeeklyShiftTemplateDetail
from resource_manager.models import Resource, ResourceGroup


def import_jobs_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Example Job structure:
        # {
        #     "id": 28831723,
        #     "name": "909",
        #     "duedate": "2024-10-01",
        #     "manualpriority": null,
        #     "type": "Sales Order"
        # },

        job_type = JobType.objects.create(name="Sales Order")

        for job in data:
            created_obj = Job.objects.create(
                external_id=job["id"],
                name=job["name"],
                due_date=job["duedate"],
                priority=job["manualpriority"],
                job_type=job_type,
            )
            print(f"JOB: {created_obj}")

        return True


def import_weekly_work_schedule_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Example schedule structure:
        # {
        #     "Id": 4,
        #     "Title": "Polish Default",
        #     "ResourceList": [],
        #     "ScheduleDetailsList": []
        # }

        for schedule in data:
            if schedule.get("Title") is not None:
                template = WeeklyShiftTemplate.objects.create(
                    external_id=schedule["Id"],
                    name=schedule.get("Title"),
                )
                print(f"WEEKLY SHIFT TEMPLATE: {template}")

        return True


def import_schedule_details_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Example schedule detail structure:
        # {
        #     "Id": 1,
        #     "Title": "Mon: 6:30-15:15",
        #     "Weekday": "Monday",
        #     "start_time": "06:30:00",
        #     "end_time": "14:45:00",
        #     "WeeklyWorkScheduleList": [
        #         {
        #             "Id": 1,
        #             "Title": "Default"
        #         },
        #         {
        #             "Id": 12,
        #             "Title": "Robot other"
        #         }
        #     ]
        # },

        for detail in data:
            for shift in detail["WeeklyWorkScheduleList"]:
                template_detail = WeeklyShiftTemplateDetail.objects.create(
                    external_id=detail["Id"],
                    weekly_shift_template=WeeklyShiftTemplate.objects.get(
                        external_id=shift["Id"]
                    ),
                    day_of_week=detail["Weekday"],
                    start_time=datetime.datetime.strptime(
                        detail["start_time"], "%H:%M:%S"
                    ),
                    end_time=datetime.datetime.strptime(detail["end_time"], "%H:%M:%S"),
                )
                print(f"SCHEDULE DETAILS: {template_detail}")

        return True


def import_resource_groups_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Example Resource Group structure:
        # {
        #     "Id": 1,
        #     "Name": "Welding Mild Steel Team 1",
        #     "Resources": [
        #         {
        #             "Id": 23,
        #             "Title": "Brian Wisborg"
        #         },
        #         {
        #             "Id": 103,
        #             "Title": "Jacob Madsen"
        #         },
        #         {
        #             "Id": 150,
        #             "Title": "Nikolaj Jensen"
        #         }
        #     ]
        # },

        for resource_group in data:
            created_obj = ResourceGroup.objects.create(
                external_id=resource_group["Id"],
                name=resource_group["Name"],
            )
            print(f"RESOURCE GROUP: {created_obj}")

        return True


def import_resources_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Example Resource structure:
        # {
        #     "Id": 1,
        #     "Name": "Adrian Cieslak",
        #     "WeeklyWorkScheduleId": 7.0,
        #     "ResourceGroupList": [
        #         {
        #             "Id": 99,
        #             "Name": "Lathing - Operators"
        #         }
        #     ]
        # },

        for resource in data:
            schedule = None
            if resource.get("WeeklyWorkScheduleId") is not None:
                schedule = int(resource["WeeklyWorkScheduleId"])

            try:
                shift_template = WeeklyShiftTemplate.objects.get(name="Default")
                if WeeklyShiftTemplate.objects.filter(external_id=schedule).exists():
                    shift_template = WeeklyShiftTemplate.objects.get(
                        external_id=schedule
                    )

                created_obj = Resource.objects.create(
                    external_id=resource["Id"],
                    name=resource["Name"],
                    weekly_shift_template=shift_template,
                )

                group_ids = [group["Id"] for group in resource["ResourceGroupList"]]

                created_obj.related_resources.set(
                    ResourceGroup.objects.filter(id__in=group_ids)
                )

                print(f"RESOURCE: {created_obj}")
            except Exception as e:
                print(f"ERROR: {e} - {resource}")
    return True


def import_items_from_json(file_path):
    # Expected Item structure:
    # {
    #     "id": 133336,
    #     "item_name": "071-053-001"
    # },
    limit = 500
    with open(file_path, "r") as file:
        data = json.load(file)
        for resource in data:
            created_obj = Item.objects.create(
                external_id=resource["id"],
                name=resource["item_name"],
            )

            print(f"ITEM: {created_obj}")

            limit = limit - 1
            if limit == 0:
                break
    return True


def import_work_center_from_json(file_path):
    # Expected Item structure:
    # {
    #     "Id": 1,
    #     "Title": "Afsyring - overfladebehandling",
    #     "ResourceAssignmentRulesList": [
    #         {
    #             "Id": 6,
    #             "RuleName": "Afsyring - overfladebehandling"
    #         },
    #         {
    #             "Id": 78,
    #             "RuleName": "04 Disc - Wash"
    #         }
    #     ]
    # },
    with open(file_path, "r") as file:
        data = json.load(file)
        for resource in data:
            print("DATA:")
            created_obj = WorkCenter.objects.create(
                external_id=resource["Id"],
                name=resource["Title"],
            )

            print(f"WORK CENTER: {created_obj}")
    return True


def import_resource_assignment_rule_from_json(file_path):
    # Expected resource_assignment_rule structure:
    # {
    #     "Id": 6,
    #     "RuleName": "Afsyring - overfladebehandling",
    #     "NeededResources": null,
    #     "UseAllResources": false,
    #     "WorkCenterId": 1,
    #     "ResourceGroups": [
    #         {
    #             "Id": 9,
    #             "Name": "Afsyring - overfladebehandling"
    #         }
    #     ],
    #     "ItemCollections": [
    #         {
    #             "Id": 168,
    #             "Title": "All Items"
    #         }
    #     ]
    # },
    with open(file_path, "r") as file:
        data = json.load(file)
        for assignment_rule in data:
            try:
                created_obj = AssigmentRule.objects.create(
                    external_id=assignment_rule["Id"],
                    name=assignment_rule["RuleName"],
                    work_center=WorkCenter.objects.get(
                        external_id=assignment_rule["WorkCenterId"]
                    ),
                    is_active=True,
                )
            except Exception as e:
                print(f"ERROR: {e} - {assignment_rule}")

            print(f"WORK CENTER: {created_obj}")
            group = assignment_rule["ResourceGroups"][0]
            try:
                resource_count = 1
                if assignment_rule["NeededResources"] is not None:
                    resource_count = assignment_rule["NeededResources"]

                created_constraint = AssignmentConstraint.objects.create(
                    assignment_rule=created_obj,
                    resource_group=ResourceGroup.objects.get(external_id=group["Id"]),
                    use_all_resources=assignment_rule["UseAllResources"],
                    resource_count=resource_count,
                )
                print(f"RULE CONSTRAINT: {created_constraint}")
            except Exception as e:
                print(f"ERROR: {e} - {group}")
        return True


def import_item_collections_from_json(file_path):
    # Expected item_collection structure:
    # {
    #     "Id": 158,
    #     "Title": "Disc Cooker: Complete Disc: Triangle Plate",
    #     "item_first_part": "1-3",
    #     "item_middle_part": "100-107",
    #     "item_last_part": null,
    #     "sequence_number": null,
    #     "item_description_starts_with": "Complete Disc",
    #     "item_description_contains": null,
    #     "ResourceAssignmentRulesList": []
    # },
    with open(file_path, "r") as file:
        data = json.load(file)
        for item_collection in data:
            try:
                for rule in item_collection["ResourceAssignmentRulesList"]:
                    if item_collection["item_first_part"] is not None:
                        created_obj = AssigmentRuleCriteria.objects.create(
                            assigment_rule=AssigmentRule.objects.get(
                                external_id=rule["Id"]
                            ),
                            field="item.name",
                            operator="starts_with",
                            value=item_collection["item_first_part"],
                        )
                    if item_collection["item_middle_part"] is not None:
                        created_obj = AssigmentRuleCriteria.objects.create(
                            assigment_rule=AssigmentRule.objects.get(
                                external_id=rule["Id"]
                            ),
                            field="item.name",
                            operator="contains",
                            value=f"-{item_collection['item_middle_part']}-",
                        )
                    if item_collection["item_last_part"] is not None:
                        created_obj = AssigmentRuleCriteria.objects.create(
                            assigment_rule=AssigmentRule.objects.get(
                                external_id=rule["Id"]
                            ),
                            field="item.name",
                            operator="ends_with",
                            value=item_collection["item_last_part"],
                        )
                    if item_collection["item_description_starts_with"] is not None:
                        created_obj = AssigmentRuleCriteria.objects.create(
                            assigment_rule=AssigmentRule.objects.get(
                                external_id=rule["Id"]
                            ),
                            field="item.description",
                            operator="starts_with",
                            value=item_collection["item_description_starts_with"],
                        )
                    if item_collection["item_description_contains"] is not None:
                        created_obj = AssigmentRuleCriteria.objects.create(
                            assigment_rule=AssigmentRule.objects.get(
                                external_id=rule["Id"]
                            ),
                            field="item.description",
                            operator="contains",
                            value=item_collection["item_description_contains"],
                        )
                    print(created_obj)
            except Exception as e:
                print(f"ERROR: {e} - {item_collection}")
        return True


def import_tasks_from_json(file_path):
    # Expected Task structure:
    # {
    #     "id": 476831,
    #     "job_id": 33799990,
    #     "name": "WO134837-30",
    #     "setuptime": 30,
    #     "duration": 30,
    #     "quantity": 1,
    #     "item_id": 720172,
    #     "workcenter_id": 9,
    #     "predecessor_ids": [
    #         476830
    #     ]
    # },
    Task.objects.all().delete()
    with open(file_path, "r") as file:
        data = json.load(file)

        for task_data in data:
            item = Item.objects.filter(external_id=task_data["item_id"])

            if len(item) > 0:
                task_item = Item.objects.filter(
                    external_id=task_data["item_id"]
                ).first()

                try:
                    created_obj = Task.objects.create(
                        external_id=task_data["id"],
                        name=task_data["name"],
                        duration=task_data["duration"],
                        setup_time=task_data["setuptime"],
                        teardown_time=60,
                        quantity=task_data["quantity"],
                        item=task_item,
                        item_id=task_item.id,
                        work_center=WorkCenter.objects.get(
                            external_id=task_data["workcenter_id"]
                        ),
                        job=Job.objects.get(external_id=task_data["job_id"]),
                    )

                    created_obj.predecessors.set(
                        Task.objects.filter(
                            external_id__in=task_data["predecessor_ids"]
                        )
                    )

                    print(f"TASK: {created_obj}")
                except Exception as e:
                    print(
                        f"ERROR: {e} - {task_data}; {task_item}; {task_data['item_id']}"
                    )
    return True


json_file_path = "/workspaces/factryflow/src/scripts/nocodb"

# Comment-out lines to skip importing data for those models
import_jobs_from_json(f"{json_file_path}/jobs.json")
import_weekly_work_schedule_from_json(f"{json_file_path}/weeklyworkschedule.json")
import_schedule_details_from_json(f"{json_file_path}/scheduledetails.json")
import_resource_groups_from_json(f"{json_file_path}/resourcegroups.json")
import_resources_from_json(f"{json_file_path}/resources.json")

import_items_from_json(f"{json_file_path}/items.json")
import_work_center_from_json(f"{json_file_path}/workcenter.json")

import_resource_assignment_rule_from_json(
    f"{json_file_path}/resourceassignmentrules.json"
)
import_item_collections_from_json(f"{json_file_path}/itemcollections.json")

import_tasks_from_json(f"{json_file_path}/tasks.json")
