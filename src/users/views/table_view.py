import datetime

from common.utils.views import (
    convert_date_to_readable_string,
    convert_datetime_to_readable_string,
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from users.models import User


class UserTableView:
    """
    Class representing a custom view for displaying tables in a generic format.
    """

    def __init__(
        self,
        model,
        model_name,
        fields,
        headers,
        search_fields_list,
        page_size=5,
        model_relation_headers=[],
        model_relation_fields={},
        status_choices_class=None,
        status_filter_field=None,
        tailwind_classes=None,
        status_classes={},
    ):
        """
        Args:
            model: The Django model class for which the table view is created.
            model_name: The name of the model.
            fields: List of fields to be displayed in the table.
            headers: List of headers for the table columns.
            status_filter_field: The field used for filtering by status.
            search_fields_list: List of fields to be searched.
            tailwind_classes: Dictionary mapping model statuses to Tailwind CSS classes.
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
        self.model_relation_headers = model_relation_headers
        self.model_relation_fields = model_relation_fields
        self.table_headers = headers
        self.page_size = page_size
        self.status_classes = status_classes

    @property
    def all_instances(self):
        """
        Retrieve all instances of the model.
        """
        return self.model.objects.all().order_by("id")

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()

    def get_all_many_to_many_field_instances(
        self, obj_instance, field_name=None, view_mode=False
    ):
        # if field is none, get for first header
        rows = []

        if field_name:
            if len(self.model_relation_fields[field_name]) == 4:
                data = self.model_relation_fields[field_name][0].objects.filter(
                    **{self.model_relation_fields[field_name][1]: obj_instance}
                )

            elif len(self.model_relation_fields[field_name]) == 3:
                data = getattr(
                    obj_instance, self.model_relation_fields[field_name][0]
                ).all()

            for instance in data:
                row_data = []
                for field in self.model_relation_fields[field_name][-1]:
                    if "status" in field:
                        value = (
                            f'<span class="{self.get_status_colored_text(getattr(instance, field))} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">'
                            f'{getattr(instance, "get_" + field + "_display")()}</span>',
                        )
                        row_data.append(value[0])
                    elif isinstance(getattr(instance, field), datetime.datetime):
                        value = convert_datetime_to_readable_string(
                            getattr(instance, field)
                        )
                        row_data.append(value)
                    elif isinstance(getattr(instance, field), datetime.date):
                        value = convert_date_to_readable_string(
                            getattr(instance, field)
                        )
                        row_data.append(value)
                    else:
                        value = getattr(instance, field)
                        row_data.append(value)
                rows.append(row_data)

        return rows

    def filtered_instances(
        self,
        status_filter=None,
        search_query=None,
    ):
        """
        Get filtered instances based on status and search query.

        Args:
            status_filter: Optional. The status filter to be applied.
            search_query: Optional. The search query to be applied.

        Returns:
            List: Filtered instances based on the provided status and search query.
        """
        all_instances = self.all_instances
        if status_filter != "all":
            all_instances = [
                instance
                for instance in all_instances
                if instance.__dict__[self.status_filter_field] == status_filter
            ]
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

    def get_paginated_instances(
        self, page_number, status_filter=None, search_query=None
    ):
        """
        Get paginated instances based on the page number and filtering.

        Args:
            page_number: The page number for paginating the instances.
            status_filter: Optional. The status filter to be applied.
            search_query: Optional. The search query to be applied.

        Returns:
            List: Paginated instances based on the provided page number and filtering.
        """
        instances = self.filtered_instances(status_filter, search_query)
        paginator = Paginator(instances, self.page_size)
        try:
            paginated_instances = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_instances = paginator.page(1)
        except EmptyPage:
            paginated_instances = paginator.page(paginator.num_pages)
        return paginated_instances

    def table_rows(
        self,
        page_number,
        status_filter=None,
        search_query=None,
    ):
        """
        Get the rows of data for the table based on the model and fields.

        Args:
            status_filter: Optional. The status filter to be applied.
            search_query: Optional. The search query to be applied.

        Returns:
            List: Rows of data for the table based on the filtered instances.
        """
        paginated_data = self.get_paginated_instances(
            page_number, status_filter, search_query
        )

        rows = []
        for instance in paginated_data.object_list:
            row_data = []
            for field in self.fields:
                if "status" in field:
                    value = (
                        f'<span class="{self.get_status_colored_text(getattr(instance, field))} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">'
                        f'{getattr(instance, "get_" + self.model_name + "_status_display")() if hasattr(instance, "get_" + self.model_name + "_status_display") else self.status_classes.get(getattr(instance, field))}</span>',
                    )
                    # value = getattr(instance, field)
                    row_data.append(value[0])
                elif isinstance(getattr(instance, field), datetime.datetime):
                    value = convert_datetime_to_readable_string(
                        getattr(instance, field)
                    )
                    row_data.append(value)
                elif isinstance(getattr(instance, field), datetime.date):
                    value = convert_date_to_readable_string(getattr(instance, field))
                    row_data.append(value)
                else:
                    value = getattr(instance, field)
                    row_data.append(value)

            rows.append(row_data)

        return rows, paginated_data

    def get_status_colored_text(self, model_status):
        """
        Get the colored text based on model status.

        Args:
            model_status: The status of the model.

        Returns:
            str: The Tailwind CSS class for the given model status.
        """
        return self.tailwind_classes.get(model_status)


USER_MODEL_FIELDS = ["id", "email", "first_name", "last_name", "is_active"]

USER_SEARCH_FIELDS = ["email", "first_name", "last_name", "is_active"]
USER_TABLE_HEADERS = ["ID", "E-mail", "First Name", "Last Name", "Active"]

USER_TABLE_VIEW = UserTableView(
    model=User,
    model_name="users",
    fields=USER_MODEL_FIELDS,
    headers=USER_TABLE_HEADERS,
    search_fields_list=USER_SEARCH_FIELDS,
)