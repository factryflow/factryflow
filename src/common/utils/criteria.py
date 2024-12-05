from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from common.models import NestedCriteriaGroup, NestedCriteria, Operator, LogicalOperator
from common.utils.constants import OPERATOR_MAPPINGS


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

    if nested_groups.count() > 0:
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


def get_all_nested_group_ids(group):
    """
    Recursively retrieves all nested group IDs for a given group instance.

    Args:
        group (NestedCriteriaGroup): The group instance for which to retrieve nested group IDs.

    Returns:
        list: A list of nested group IDs.
    """
    group_ids = [group.id]
    nested_groups = NestedCriteriaGroup.objects.filter(parent_group=group)

    if nested_groups.count() > 0:
        for nested_group in nested_groups:
            group_ids.extend(get_all_nested_group_ids(nested_group))

    return group_ids


def build_nested_query(group):
    """
    Builds a fully nested Q object for a given NestedCriteriaGroup, including handling of related fields.
    """
    query = Q()

    # iterate through all nested criteria in the group
    for nested_criteria in group.nested_group.all():
        if nested_criteria.related_criteria:
            # handle individual criteria
            related_criteria = nested_criteria.related_criteria
            field = related_criteria.field
            operator = related_criteria.operator
            value = related_criteria.value

            # construct the filter key
            if "." in field:
                # handle related fields with dot notation
                related_field, subfield = field.split(".", 1)
                filter_key = (
                    f"{related_field}__{subfield}{OPERATOR_MAPPINGS.get(operator, '')}"
                )
            else:
                filter_key = f"{field}{OPERATOR_MAPPINGS.get(operator, '')}"

            if operator == Operator.IN_BETWEEN:
                value_parts = value.split("-")  # split range into start and end
                query_part = Q(**{filter_key: (value_parts[0], value_parts[1])})
            else:
                query_part = Q(**{filter_key: value})

            # combine query parts based on the logical operator
            if group.operator == LogicalOperator.AND:
                query &= query_part
            else:
                query |= query_part
        elif nested_criteria.group:
            # recursively handle nested groups
            nested_query = build_nested_query(nested_criteria.group)
            if group.operator == LogicalOperator.AND:
                query &= nested_query
            else:
                query |= nested_query

    # nested groups directly related to this group
    for child_group in group.nested_groups.all():
        child_query = build_nested_query(child_group)
        if group.operator == LogicalOperator.AND:
            query &= child_query
        else:
            query |= child_query

    return query
