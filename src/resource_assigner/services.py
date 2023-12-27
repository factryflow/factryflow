from .models import TaskResourceAssigment, AssigmentRule, AssigmentRuleCriteria, Operator
from job_manager.models import Task, WorkCenter
from resource_manager.models import Resource, ResourceGroup
from common.services import model_update
from django.db import transaction


class TaskResourceAssigmentService:
    def __init__(self) -> None:
        pass

    @transaction.atomic
    def create(
        self,
        *,
        task:Task,
        use_all_resources: bool = True,
        resource_count: int = None,
        resource_group:ResourceGroup,
        resources: list[Resource] = None,
        is_direct: bool = False,
    ):
        
        task_resource_assignment = TaskResourceAssigment.objects.create(
            task=task,
            resource_group=resource_group,
            use_all_resources=use_all_resources,
            is_direct=is_direct,
        )

        if resources:
            task_resource_assignment.resources.set(resources)

        if resource_count:
            task_resource_assignment.resource_count = resource_count

        task_resource_assignment.save()

        return task_resource_assignment

    @transaction.atomic
    def update(self, *, instance: TaskResourceAssigment, data: dict):
        fields = ["task", "resource_group", "resources", "resource_count", "use_all_resources", "is_direct" ]
        
        task_resource_assignment, _ = model_update(instance=instance, fields=fields, data=data)
        return task_resource_assignment

    def delete(self, instance: TaskResourceAssigment):
        instance.delete()



class AssigmentRuleService:
    def __init__(self) -> None:
        pass

    @transaction.atomic
    def create(
        self,
        *,
        name:str,
        description:str = "",
        resource_group:ResourceGroup,
        work_center:WorkCenter,
    ):

        assignment_rule = AssigmentRule.objects.create(
            name=name,
            description= description,
            resource_group=resource_group,
            work_center=work_center,
        )
        assignment_rule.save()

        return assignment_rule

    @transaction.atomic
    def update(self, instance: AssigmentRule, data: dict):

        fields = ["name", "description", "resource_group", "work_center"]
        assignment_rule, _ = model_update(instance=instance, fields=fields, data=data)
        return assignment_rule

    def delete(self, instance: AssigmentRule):
        instance.delete()



class AssigmentRuleCriteriaService:
    def __init__(self) -> None:
        pass

    @transaction.atomic
    def create(
        self, 
        assigment_rule: AssigmentRule, 
        field: str,
        operator: Operator,
        value: str = ""
        ):
        assignment_rule_criteria = AssigmentRuleCriteria.objects.create(
            assigment_rule=assigment_rule, 
            field=field,
            operator=operator,
            value=value,
        )
        assignment_rule_criteria.save()

        return assignment_rule_criteria

    @transaction.atomic
    def update(self, instance: AssigmentRuleCriteria, data: dict):
        fields = ["assigment_rule", "field", "operator", "value"]
        assignment_rule_criteria, _ = model_update(instance=instance, fields=fields, data=data)
        return assignment_rule_criteria

    def delete(self, instance: AssigmentRuleCriteria):
        instance.delete()
