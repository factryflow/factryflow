from django.contrib.contenttypes.models import ContentType
from common.models import NestedCriteriaGroup, NestedCriteria


def get_nested_criteria(model, id):
    """
    Retrieve nested criteria for a given model and id.

    This function fetches the nested criteria associated with a specific model and id.
    It first determines the content type of the model, then retrieves the parent group
    of nested criteria. If a parent group exists, it gathers the nested group data and
    appends it to the nested_criteria list.

    Args:
        model (Model): The Django model for which nested criteria are to be retrieved.
        id (int): The ID of the specific instance of the model.

    Returns:
        list: A list of nested criteria data.
    """
    nested_criteria = []

    # get the content type of the model
    content_type = ContentType.objects.get_for_model(model)

    # get the parent group
    parent_group = NestedCriteriaGroup.objects.filter(
        content_type=content_type, object_id=id, parent_group__isnull=True
    )

    if parent_group.count() != 0:
        for group in parent_group:
            group_data = get_nested_group_data(group)
            nested_criteria.append(group_data)

    return nested_criteria


def get_nested_group_data(group_instance):
    """
    Recursively retrieves and constructs a nested dictionary representation of a group instance and its nested groups.

    Args:
        group_instance (Group): The group instance for which to retrieve nested group data.

    Returns:
        dict: A dictionary containing the group's id, operator, criteria, and any inner nested groups.
    """
    group_data = {
        "id": group_instance.id,
        "operator": group_instance.operator,
        "criteria": get_nested_criteria_for_group(group_instance),
        "innerGroups": [],
    }

    nested_groups = NestedCriteriaGroup.objects.filter(parent_group=group_instance)

    if nested_groups.count() != 0:
        for nested_group in nested_groups:
            nested_group_data = get_nested_group_data(nested_group)
            group_data["innerGroups"].append(nested_group_data)

    return group_data


def get_nested_criteria_for_group(group_instance):
    """
    Retrieve nested criteria for a given group instance.

    Args:
        group_instance (Group): The group instance for which to retrieve nested criteria.

    Returns:
        list: A list of dictionaries, each containing the following keys:
            - id (int): The object ID of the criteria.
            - field (str): The field name of the related criteria.
            - operator (str): The operator of the related criteria.
            - value (str): The value of the related criteria.
    """
    group_criteria = []

    criterias = NestedCriteria.objects.filter(group=group_instance)
    for criteria in criterias:
        criteria_data = {
            "id": criteria.object_id,
            "field": criteria.related_criteria.field,
            "operator": criteria.related_criteria.operator,
            "value": criteria.related_criteria.value,
        }
        group_criteria.append(criteria_data)

    return group_criteria
