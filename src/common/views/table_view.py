from datetime import date, datetime, time

from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from common.models import CustomField
from common.utils.views import convert_timestamp, convert_date

# ------------------------------------------------------------------------------
# CustomTableView:
#    CustomTableView is a class that provides a generic way to display Django model
#    instances in a tabular format. It supports features like pagination, filtering,
#    searching, and custom field handling.
# ------------------------------------------------------------------------------


class CustomTableView:
    """
    Class representing a custom view for displaying tables in a generic format.
    """

    def __init__(
        self,
        model,
        model_name,
        fields,
        search_fields_list,
        model_relation_headers=[],
        model_relation_fields={},
        status_choices_class=None,
        status_filter_field=None,
        tailwind_classes=None,
        status_classes={},
        order_by_field="",
    ):
        """
        Args:
            model: The Django model class for which the table view is created.
            model_name: The name of the model.
            fields: List of fields to be displayed in the table.
            headers: List of headers for the table columns.
            search_fields_list: List of fields to be searched.
            model_relation_headers: List of headers for related models.
            model_relation_fields: Dictionary mapping related model fields.
            status_choices_class: Class containing status choices.
            status_filter_field: The field used for filtering by status.
            tailwind_classes: Dictionary mapping model statuses to Tailwind CSS classes.
            status_classes: Dictionary mapping statuses to their display names.
            order_by_field: Field to order the instances by.
        """
        self.model = model
        self.model_name = model_name
        self.status_filter_field = status_filter_field
        self.search_fields_list = search_fields_list
        self.status_filter_dict = (
            status_choices_class.to_dict() if status_choices_class else {}
        )
        self.tailwind_classes = tailwind_classes
        self.fields = fields
        self.model_relation_headers = (
            model_relation_headers + ["CUSTOM_FIELDS"]
            if hasattr(self.model, "custom_fields")
            else []
        )
        self.model_relation_fields = model_relation_fields
        self.table_headers = fields
        self.status_classes = status_classes
        self.order_by_field = order_by_field

    @property
    def all_instances(self):
        """
        Retrieve all instances of the model, ordered by the specified field if it exists.

        Returns:
            QuerySet: A Django QuerySet containing all instances of the model, ordered by the specified field.
        """
        return self.model.objects.all()

    def get_custom_field_json_data(self, instance=None):
        """
        Retrieve custom field JSON data for a given instance.

        Args:
            instance (Model, optional): The model instance containing custom fields. Defaults to None.

        Returns:
            list: A list of dictionaries containing custom field information with the following keys:
                - id (int): The unique identifier for the custom field.
                - name (str): The name of the custom field.
                - label (str): The label of the custom field.
                - type (str): The type of the custom field, formatted with spaces instead of hyphens or underscores.
                - value (str): The value of the custom field, formatted as a readable string if it is a date or datetime field.
        """
        custom_field_data = instance.custom_fields
        data = []
        id = 0
        if custom_field_data:
            for key, value in custom_field_data.items():
                id += 1
                field_info = {}
                custom_field_instance = CustomField.objects.get(
                    name=key, content_type=ContentType.objects.get_for_model(instance)
                )
                field_info["id"] = id
                field_info["name"] = custom_field_instance.name
                field_info["label"] = custom_field_instance.label
                field_info["type"] = (
                    custom_field_instance.field_type.title()
                    .replace("-", " ")
                    .replace("_", " ")
                )
                if custom_field_instance.field_type == "datetime-local":
                    # convert datetime field to readable string
                    field_info["value"] = str(
                        convert_timestamp(datetime.strptime(value, "%Y-%m-%dT%H:%M"))
                    )
                elif custom_field_instance.field_type == "date":
                    # convert date field to readable string
                    field_info["value"] = str(datetime.strptime(value, "%Y-%m-%d"))
                else:
                    field_info["value"] = value

                data.append(field_info)
        return data

    def get_all_many_to_many_field_instances(self, obj_instance, field_name=None):
        """
        Retrieve all instances of many-to-many fields for a given object instance.

        Args:
            obj_instance (Model): The instance of the model for which many-to-many field instances are to be retrieved.
            field_name (str, optional): The name of the many-to-many field. Defaults to None.

        Returns:
            list: A list of dictionaries where each dictionary represents a row of data with field values and their types.
        """
        rows = []

        if field_name == "custom_fields":
            data = self.get_custom_field_json_data(obj_instance)
            formatted_data = []
            for item in data:
                formatted_item = {}
                for key, value in item.items():
                    field_type = type(value).__name__
                    formatted_item[key] = {"value": str(value), "type": field_type}
                formatted_data.append(formatted_item)
            return formatted_data

        if field_name:
            if "model" in self.model_relation_fields[field_name].keys():
                # if model is provided in model_relation_fields then get data from that model
                data = self.model_relation_fields[field_name]["model"].objects.filter(
                    **{
                        self.model_relation_fields[field_name][
                            "related_name"
                        ]: obj_instance
                    }
                )
            else:
                # if model is not provided in model_relation_fields then get data from related_name
                data = getattr(
                    obj_instance, self.model_relation_fields[field_name]["related_name"]
                ).all()

            for instance in data:
                # get data for each field in the model
                row_data = {}
                for field in self.model_relation_fields[field_name]["fields"]:
                    if "status" in field:
                        # if field is status field then get the colored text
                        value = {
                            "value": str(
                                getattr(instance, "get_" + field + "_display")()
                            ),
                            "type": "text",
                        }
                        row_data[field] = value
                    elif isinstance(getattr(instance, field), datetime):
                        # if field is datetime then convert it to readable string and type is datetime-local
                        value = {
                            "value": str(convert_timestamp(getattr(instance, field))),
                            "type": "datetime-local",
                        }
                        row_data[field] = value
                    elif isinstance(getattr(instance, field), date):
                        # if field is date then convert it to readable string and type is date
                        value = {
                            "value": str(getattr(instance, field)),
                            "type": "datetime-local",
                        }
                        row_data[field] = value
                    elif isinstance(getattr(instance, field), time):
                        # if field is time then convert it to readable string and type is time
                        value = {
                            "value": str(getattr(instance, field).strftime("%H:%M")),
                            "type": "time",
                        }
                        row_data[field] = value
                    else:
                        # if field is not status or datetime then get the value and type
                        field_type = type(getattr(instance, field)).__name__
                        value = {
                            "value": str(getattr(instance, field)),
                        }
                        if field_type == "RelatedManager":
                            # if field type is RelatedManager then type is many_to_many
                            value["type"] = "many_to_many"
                            if hasattr(instance, "name"):
                                value["value"] = instance.name
                            else:
                                value["value"] = instance.id
                        if field_type == "str":
                            # if field type is str then type is text
                            value["type"] = "text"
                        elif (
                            field_type == "int"
                            or field_type == "AutoField"
                            or field_type == "PositiveIntegerField"
                            or field_type == "IntegerField"
                        ):
                            # if field type is int then type is number
                            value["type"] = "number"
                        else:
                            # if field type is not str or int then type is field type
                            value["type"] = field_type

                        row_data[field] = value

                    if "select_fields" in self.model_relation_fields[field_name]:
                        # if select_fields is provided in model_relation_fields
                        if (
                            field
                            in self.model_relation_fields[field_name]["select_fields"]
                        ):
                            value = {
                                "value": self.model_relation_fields[field_name][
                                    "select_fields"
                                ][field][str(getattr(instance, field))],
                                "type": "select",
                                "options": self.model_relation_fields[field_name][
                                    "select_fields"
                                ][field],
                            }
                            row_data[field] = value

                rows.append(row_data)

        return rows

    def filtered_instances(
        self,
        sort_direction,
        sort_field,
        status_filter=None,
        search_query=None,
        parent_filter=None,
    ):
        """
        Get filtered instances based on status and search query.

        Args:
            status_filter (str, optional): The status filter to be applied. Defaults to None.
            search_query (str, optional): The search query to be applied. Defaults to None.

        Returns:
            list: A list of filtered instances based on the provided status and search query.
        """
        if parent_filter:
            all_instances = self.model.objects.filter(parent__isnull=True)
        else:
            all_instances = self.all_instances

        if status_filter and status_filter != "all":
            all_instances = all_instances.filter(
                **{self.status_filter_field: status_filter}
            )

        if search_query:
            all_instances = [
                instance
                for instance in all_instances
                if any(
                    search_query.lower() in str(getattr(instance, field)).lower()
                    for field in self.search_fields_list
                )
            ]
            return all_instances

        if sort_field:
            sort_prefix = "" if sort_direction == "asc" else "-"
            all_instances = all_instances.order_by(f"{sort_prefix}{sort_field}")

        if self.order_by_field:
            all_instances = all_instances.order_by(self.order_by_field)

        return all_instances

    def get_paginated_instances(
        self,
        page_number,
        sort_direction,
        sort_field,
        status_filter=None,
        search_query=None,
        num_of_rows_per_page=25,
        parent_filter=False,
    ):
        """
        Get paginated instances based on the page number and filtering.

        Args:
            page_number (int): The page number for paginating the instances.
            status_filter (str, optional): The status filter to be applied. Defaults to None.
            search_query (str, optional): The search query to be applied. Defaults to None.
            num_of_rows_per_page (int, optional): The number of rows per page. Defaults to 25.

        Returns:
            tuple: A tuple containing:
                - paginated_instances (Page): The paginated instances for the given page number.
                - num_pages (int): The total number of pages.
                - total_instances_count (int): The total number of instances.
        """
        instances = self.filtered_instances(
            sort_direction,
            sort_field,
            status_filter,
            search_query,
            parent_filter=parent_filter,
        )
        paginator = Paginator(instances, num_of_rows_per_page)
        num_pages = paginator.num_pages
        total_instances_count = paginator.count

        try:
            paginated_instances = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_instances = paginator.page(1)
        except EmptyPage:
            paginated_instances = paginator.page(paginator.num_pages)
        return paginated_instances, num_pages, total_instances_count

    def table_rows(
        self,
        page_number,
        sort_direction,
        sort_field,
        num_of_rows_per_page=25,
        status_filter=None,
        search_query=None,
        parent_filter=None,
    ):
        """
        Get the rows of data for the table based on the model and fields.

        Args:
            page_number (int): The page number for paginating the instances.
            num_of_rows_per_page (int): The number of rows per page. Default 25
            status_filter (str, optional): The status filter to be applied. Defaults to None.
            search_query (str, optional): The search query to be applied. Defaults to None.

        Returns:
            tuple: A tuple containing:
                - rows (list): Rows of data for the table based on the filtered instances.
                - paginated_data (Page): The paginated instances for the given page number.
                - num_pages (int): The total number of pages.
                - total_instances_count (int): The total number of instances.
        """
        paginated_data, num_pages, total_instances_count = self.get_paginated_instances(
            page_number,
            sort_direction,
            sort_field,
            status_filter,
            search_query,
            num_of_rows_per_page,
            parent_filter=parent_filter,
        )

        rows = []
        for instance in paginated_data.object_list:
            row_data = []
            for field in self.fields:
                if field == "order":
                    # Get order field value and increment it by 1
                    value = getattr(instance, field) + 1
                    row_data.append(value)
                elif "status" in field:
                    value = (
                        f'<span class="{self.get_status_colored_text(getattr(instance, field))} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">'
                        f'{getattr(instance, "get_" + self.model_name + "_status_display")() if hasattr(instance, "get_" + self.model_name + "_status_display") else self.status_classes.get(getattr(instance, field))}</span>',
                    )
                    row_data.append(value[0])
                elif isinstance(getattr(instance, field), datetime):
                    value = convert_timestamp(getattr(instance, field))
                    row_data.append(value)
                elif isinstance(getattr(instance, field), date):
                    value = convert_date(getattr(instance, field))
                    row_data.append(value)
                else:
                    value = getattr(instance, field)
                    row_data.append(value)

            rows.append(row_data)

        return rows, paginated_data, num_pages, total_instances_count

    def get_status_colored_text(self, model_status):
        """
        Get the colored text based on model status.

        Args:
            model_status: The status of the model.

        Returns:
            str: The Tailwind CSS class for the given model status.
        """
        return self.tailwind_classes.get(model_status)
