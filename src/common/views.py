import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.forms import inlineformset_factory

from common.utils.views import (
    add_notification_headers,
    convert_date_to_readable_string,
    convert_datetime_to_readable_string,
)

from .forms import CustomFieldForm
from .models import CustomField, FieldType
from .services import CustomFieldService


# ------------------------------------------------------------------------------
# Custom CRUDView
# ------------------------------------------------------------------------------


class CRUDView:
    """
    A generic CRUD (Create, Read, Update, Delete) view for handling various models.

    Attributes:
        model: The model.
        model_type: The type of model (optional).
        model_name: The name of the model.
        model_service: The service class handling model operations.
        model_form: The form class for the model.
        table_view: The view class for rendering model data in a tabular format.
        list_template_name: The name of the template for listing model instances.
        detail_template_name: The name of the template for displaying model details.
    """

    def __init__(
        self,
        model,
        model_name,
        model_service,
        model_form,
        model_table_view,
        formset_options=[],
        model_type=None,
        view_only=False,
        button_text="Add",
        ordered_model=False,
        user_rule_permission=True,
    ):
        self.model = model
        self.model_type = model_type
        self.view_only = view_only
        self.model_name = model_name
        self.model_title = model_name.capitalize().replace("_", " ")
        self.model_service = model_service
        self.model_form = model_form
        self.table_view = model_table_view
        self.model_type = model_type
        self.list_template_name = "objects/list.html"
        self.detail_template_name = "objects/details.html"
        self.user_rule_permission = user_rule_permission
        self.crud_action_rules = self.get_models_crud_permissions(model_name)
        self.button_text = button_text
        self.ordered_model = ordered_model
        self.formset_options = formset_options
        self.model_formset = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Dispatches the request to the appropriate view method.
        return super().dispatch(request, *args, **kwargs)

    def get_models_crud_permissions(self, model_name):
        permissions_list = (
            [
                f"view_{model_name.lower()}",
                f"add_{model_name.lower()}",
                f"change_{model_name.lower()}",
                f"delete_{model_name.lower()}",
            ]
            if model_name
            else None
        )
        return permissions_list

    def get_custom_field_json_data(self, content_type, instance=None):
        # to get custom field json data
        data = []
        id = 0
        if instance and instance.custom_fields != {}:
            custom_field_data = instance.custom_fields
            if custom_field_data:
                for key, value in custom_field_data.items():
                    id += 1
                    custom_field_instance = CustomField.objects.get(name=key)
                    field_name = custom_field_instance.name
                    field_label = custom_field_instance.label
                    field_type = custom_field_instance.field_type
                    field_info = [id, field_name, field_label, field_type, value]
                    data.append(field_info)
        else:
            custom_fields = CustomField.objects.filter(content_type=content_type)
            for custom_field in custom_fields:
                id += 1
                field_name = custom_field.name
                field_label = custom_field.label
                field_type = custom_field.field_type
                field_info = [id, field_name, field_label, field_type, ""]
                data.append(field_info)

        return data

    def get_all_instances(self, request):
        """
        View function to display all instances with optional filtering.

        Returns:
            The rendered response displaying all instances.
        """
        # Retrieve filtering and search parameters from the request
        status_filter = request.GET.get("status", "all")
        search_query = request.GET.get("query", "")
        page_number = request.GET.get("page", 1)

        # Generate table view based on filter and search parameters
        table_rows, paginator = self.table_view.table_rows(
            status_filter=status_filter,
            search_query=search_query,
            page_number=page_number,
        )

        template_name = self.list_template_name

        # Determine whether to include partial template based on request headers
        if "HX-Request" in request.headers:
            template_name += "#partial-table-template"

        context = {
            "headers": self.table_view.table_headers,
            "status_filter_dict": self.table_view.status_filter_dict,
            "rows": table_rows,
            "paginator": paginator,
            "show_actions": True and self.user_rule_permission,
            "crud_action_rules": self.crud_action_rules,
            "model_name": self.model_name,
            "model_name_for_crud": self.model_name,
            "model_title": self.model_title,
            "view_only": self.view_only,
            "button_text": self.button_text,
            "ordered_model": self.ordered_model,
        }

        return render(request, template_name, context)

    def show_model_form(
        self,
        request,
        id: int = None,
        edit: str = "",
        field: str = "",
        formset_count: int = 1,
    ):
        """
        View function to display a form for creating or editing a model instance.

        Args:
            request: The HTTP request object.
            id: The ID of the model instance (optional).
            edit: Flag indicating whether the form is in edit mode (optional).

        Returns:
            The rendered response displaying the model form.
        """
        # Determine form action URL based on whether editing or creating
        form_action_url = f"/{self.model_name.replace('_', '-').lower()}-create/"

        relation_field_name = None

        # get content type using self.model
        model_content_type = ContentType.objects.get_for_model(self.model)

        # get field parameter
        if len(self.table_view.model_relation_headers) > 0:
            relation_field_name = (
                self.table_view.model_relation_headers[0].lower().replace(" ", "_")
            )

        if field:
            relation_field_name = field.lower()

        # model inline formset for one-to-many relation
        if len(self.formset_options) > 0:
            self.model_formset = inlineformset_factory(
                self.model,
                self.formset_options[0],
                form=self.formset_options[1],
                extra=formset_count,
                can_delete=False,
            )

        custom_field_form_data = self.get_custom_field_json_data(
            content_type=model_content_type
        )

        # Process the form based on ID and edit mode
        rows = []
        if id:
            instance_obj = get_object_or_404(self.model, id=id)
            form = self.model_form(instance=instance_obj)
            if "name" in instance_obj.__dict__:
                page_label = instance_obj.name.capitalize().replace("_", " ")
            else:
                page_label = f"{self.model_title} Details"

            custom_field_form_data = self.get_custom_field_json_data(
                model_content_type, instance_obj
            )

            # self.table_view.get_all_many_to_field_instances(instance_obj)
            if edit != "true":
                view_mode = True
                form_label = f"{self.model_title} Details"
                button_text = "Edit"
                edit_url = (
                    reverse(f"edit_{self.model_name.lower()}", args=[id, "true"])
                    if self.user_rule_permission
                    else None
                )

                # Make all form fields read-only
                for field in form.fields.values():
                    field.widget.attrs["disabled"] = True

            else:
                button_text = "Save"
                form_label = f"{self.model_title} Details"
                view_mode = False

            rows = (
                self.table_view.get_all_many_to_many_field_instances(
                    instance_obj, relation_field_name
                )
                if relation_field_name
                else []
            )

        else:
            form = self.model_form()
            button_text = "Create"
            view_mode = False
            form_label = f"New {self.model_title} Details"
            page_label = f"New {self.model_title}"

        relation_table_headers = (
            ["ID", "Name", "Label", "Type", "Value"]
            if relation_field_name == "custom_fields"
            else self.table_view.model_relation_fields[relation_field_name]["headers"]
        )

        # model name of relation field
        relation_model_name = (
            self.table_view.model_relation_fields[relation_field_name].get("model_name")
            if relation_field_name not in ["custom_fields", "history"]
            else None
        )

        # add and remove urls for formset
        if len(self.formset_options) > 0:
            add_formset_url = (
                reverse(
                    f"{self.model_name.lower()}_formset",
                    args=[formset_count + 1],
                )
                if self.user_rule_permission
                else None
            )

            remove_formset_url = (
                reverse(
                    f"{self.model_name.lower()}_formset",
                    args=[formset_count - 1],
                )
                if self.user_rule_permission
                else None
            )

        context = {
            "form": form,
            "formset_title": self.formset_options[2] if self.formset_options else None,
            "formset_form": self.model_formset() if self.model_formset else None,
            "add_formset_url": add_formset_url
            if "add_formset_url" in locals()
            else None,
            "remove_formset_url": remove_formset_url
            if "remove_formset_url" in locals()
            else None,
            "view_mode": view_mode,
            "view_only": self.view_only,
            "form_label": form_label,
            "button_text": button_text,
            "form_action_url": form_action_url,
            "id": id if id else None,
            "edit_url": edit_url if "edit_url" in locals() else None,
            "page_label": page_label,
            "model_name": self.model_name,
            "model_name_for_crud": relation_model_name,
            "crud_action_rules": self.get_models_crud_permissions(relation_model_name),
            "model_title": self.model_title,
            "field_url": self.model_name.replace("_", "-").lower(),
            "custom_field_data": custom_field_form_data
            if custom_field_form_data
            else None,
            "show_actions": True if edit == "true" and relation_model_name else False,
            "headers": relation_table_headers if relation_field_name else [],
            "relations_headers": self.table_view.model_relation_headers,
            "rows": rows,
        }

        if "HX-Request" in request.headers:
            # if formset_count in the request as path parameters then return details page with #new-row-formset
            if "field" in str(request.path):
                return render(
                    request,
                    f"{self.list_template_name}#partial-table-template",
                    context,
                )

            if "formset" in str(request.path):
                return render(
                    request,
                    f"{self.detail_template_name}",
                    context,
                )

        return render(
            request,
            self.detail_template_name,
            context,
        )

    # @require_http_methods('POST')
    def create_or_update_model_instance(self, request, id: int = None):
        """
        Handle POST request to create or update a model instance using Django form and service.

        Args:
            request: The HTTP request object.
            id: The ID of the model instance (optional).

        Returns:
            The response indicating success or failure of the operation.
        """
        # get instance object id
        id = request.POST.get("id")

        # custom field data
        custom_fields_keys = request.POST.getlist("key[]")
        custom_fields_values = request.POST.getlist("value[]")

        custom_fields_data = dict(zip(custom_fields_keys, custom_fields_values))

        # Get the instance object if updating, otherwise None
        instance_obj = get_object_or_404(self.model, id=id) if id else None

        # Instantiate the form with POST data and optionally the instance object
        form = self.model_form(
            request.POST, instance=instance_obj if instance_obj else None
        )

        if len(form.errors) > 0:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            for field, error in errors.items():
                response = HttpResponse(status=400)
                message = f"{field}: {error[0]['message']}"
                add_notification_headers(response, message, "error")

            return response

        # inline formset validation and data fetching
        formset_data = []

        # check if formset form is available
        if len(self.formset_options) > 0:
            # get total number of forms in formset
            total_formset_forms = int(
                request.POST.get(f"{self.formset_options[2]}-TOTAL_FORMS", 0)
            )

            if total_formset_forms > 0:
                # errors handling
                inline_model_form = self.model_formset(request.POST or None)

                for inline_form in inline_model_form:
                    if inline_form.errors:
                        errors = {
                            f: e.get_json_data() for f, e in inline_form.errors.items()
                        }
                        for field, error in errors.items():
                            response = HttpResponse(status=400)
                            message = f"{field}: {error[0]['message']}"
                            add_notification_headers(response, message, "error")

                        return response

                    if inline_model_form.is_valid():
                        # if inline form is valid, get the form data
                        for inline_form in inline_model_form:
                            data_dict = {}
                            form_data = inline_form.cleaned_data
                            for key, value in form_data.items():
                                if key in self.formset_options[3]:
                                    data_dict[key] = value
                            formset_data.append(data_dict)

        if form.is_valid():
            # Extract data from the form
            obj_data = form.cleaned_data
            
            # if custom_fields_data != {}:
            obj_data["custom_fields"] = custom_fields_data

            # Call the service function to create or update the instance
            obj_data["id"] = id
            if len(self.formset_options) > 0 and len(formset_data) > 0:
                obj_data[self.formset_options[2]] = formset_data

            try:
                existing_instance = self.model.objects.get(id=obj_data["id"])
                self.model_service(user=request.user).update(
                    existing_instance, obj_data
                )
                message = f"{self.model_title} updated successfully!"

            except self.model.DoesNotExist:
                del obj_data["id"]
                if custom_fields_data != {}:
                    obj_data["custom_fields"] = custom_fields_data

                self.model_service(user=request.user).create(**obj_data)
                message = f"{self.model_title} created successfully!"

            # Render the form with success message and handle HX-Request
            form = self.model_form()

            response = render(
                request,
                f"{self.detail_template_name}#partial-form",
                {
                    "form": form,
                    "button_text": f"Add {self.model_title}",
                    "form_label": f"{self.model_title} Details",
                    "model_name": self.model_name,
                    "model_title": self.model_title,
                    "relations_headers": self.table_view.model_relation_headers,
                    "crud_action_rules": self.crud_action_rules,
                },
            )

            if request.htmx:
                headers = {"HX-Redirect": reverse(self.model_name.lower())}
                response = HttpResponse(status=204, headers=headers)
                add_notification_headers(
                    response,
                    message,
                    "success",
                )
                return response

    def delete_obj_instance(self, request, id):
        """
        Handle model instance deletion request.

        Args:
            request: The HTTP request object.
            id: The ID of the model instance to be deleted.

        Returns:
            The response indicating success or failure of the deletion operation.
        """
        obj = get_object_or_404(self.model, id=id)

        # Delete the instance and check if deletion was successful
        deletion_successful = self.model_service(user=request.user).delete(obj)

        # Retrieve updated instance list
        status_filter = request.GET.get("status", "all")
        search_query = request.GET.get("query", "")
        page_number = request.GET.get("page", 1)

        # Generate table view based on filter and search parameters
        table_rows, paginator = self.table_view.table_rows(
            status_filter=status_filter,
            search_query=search_query,
            page_number=page_number,
        )

        # Render the updated table and add notification headers
        response = render(
            request,
            f"{self.list_template_name}#partial-table-template",
            {
                "headers": self.table_view.table_headers,
                "status_filter_dict": self.table_view.status_filter_dict,
                "rows": table_rows,
                "paginator": paginator,
                "show_actions": True and self.user_rule_permission,
                "crud_action_rules": self.crud_action_rules,
                "ordered_model": self.ordered_model,
                "model_name": self.model_name,
                "model_name_for_crud": self.model_name,
                "model_title": self.model_title,
            },
        )

        # Add notification based on deletion success or failure
        if deletion_successful:
            add_notification_headers(
                response,
                f"{self.model_title} has been deleted.",
                "success",
            )
        else:
            add_notification_headers(
                response,
                f"Failed to delete the {self.model_title}.",
                "error",
            )

        return response


# ------------------------------------------------------------------------------
# CustomTableView for any model
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
        headers,
        search_fields_list,
        page_size=5,
        model_relation_headers=[],
        model_relation_fields={},
        status_choices_class=None,
        status_filter_field=None,
        tailwind_classes=None,
        status_classes={},
        order_by_field="id",
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
        self.model_relation_headers = (
            model_relation_headers + ["CUSTOM_FIELDS"]
            if hasattr(self.model, "custom_fields")
            else []
        )
        self.model_relation_fields = model_relation_fields
        self.table_headers = headers
        self.page_size = page_size
        self.status_classes = status_classes
        self.order_by_field = order_by_field

    @property
    def all_instances(self):
        """
        Retrieve all instances of the model.
        """
        if hasattr(self.model, self.order_by_field):
            return self.model.objects.all().order_by(self.order_by_field)

        return self.model.objects.all().order_by("id")

    def get_custom_field_json_data(self, instance=None):
        # get custom field json data in two rows one is headers which are keys(convert in captilize and replace "_" with " ", and values as data)
        # each model has extras_field as a custom field
        custom_field_data = instance.custom_fields
        data = []
        id = 0
        if custom_field_data:
            for key, value in custom_field_data.items():
                id += 1
                custom_field_instance = CustomField.objects.get(name=key)
                field_name = custom_field_instance.name
                field_label = custom_field_instance.label
                field_type = custom_field_instance.field_type
                field_info = [id, field_name, field_label, field_type, value]
                data.append(field_info)
        return data

    def get_all_many_to_many_field_instances(self, obj_instance, field_name=None):
        # if field is none, get for first header
        rows = []

        if field_name == "custom_fields":
            data = self.get_custom_field_json_data(obj_instance)
            return data

        if field_name:
            if "model" in self.model_relation_fields[field_name].keys():
                data = self.model_relation_fields[field_name]["model"].objects.filter(
                    **{
                        self.model_relation_fields[field_name][
                            "related_name"
                        ]: obj_instance
                    }
                )

            if "model" not in self.model_relation_fields[field_name].keys():
                data = getattr(
                    obj_instance, self.model_relation_fields[field_name]["related_name"]
                ).all()

            for instance in data:
                row_data = []
                for field in self.model_relation_fields[field_name]["fields"]:
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


# ------------------------------------------------------------------------------
# Custom Field Views
# ------------------------------------------------------------------------------

CUSTOM_FIELD_MODEL_FIELDS = [
    "id",
    "name",
    "label",
    "content_type",
    "field_type",
    "is_required",
    "description",
]
CUSTOM_FIELD_TABLE_HEADERS = [
    "ID",
    "Field Name",
    "Label",
    "Content Type",
    "Field Type",
    "Is Required",
    "Description",
]

CUSTOM_FIELD_SEARCH_FIELDS = ["name", "field_type", "label", "description"]


CUSTOM_FIELD_STATUS_FILTER_FIELD = "field_type"

CUSTOM_FIELD_MODEL_RELATION_HEADERS = ["HISTORY"]
CUSTOM_FIELD_MODEL_RELATION_FIELDS = {
    "history": {
        "model_name": "history",
        "related_name": "history",
        "headers": [
            "ID",
            "Name",
            "User",
            "Label",
            "Type",
            "Description",
            "History Date",
        ],
        "fields": [
            "history_id",
            "name",
            "history_user",
            "label",
            "field_type",
            "description",
            "history_date",
        ],
    },
}


CustomFieldTableView = CustomTableView(
    model=CustomField,
    model_name="custom_field",
    fields=CUSTOM_FIELD_MODEL_FIELDS,
    headers=CUSTOM_FIELD_TABLE_HEADERS,
    model_relation_headers=CUSTOM_FIELD_MODEL_RELATION_HEADERS,
    model_relation_fields=CUSTOM_FIELD_MODEL_RELATION_FIELDS,
    status_filter_field=CUSTOM_FIELD_STATUS_FILTER_FIELD,
    status_choices_class=FieldType,
    search_fields_list=CUSTOM_FIELD_SEARCH_FIELDS,
)

CUSTOM_FIELD_VIEWS = CRUDView(
    model=CustomField,
    model_name="custom_fields",
    model_service=CustomFieldService,
    model_form=CustomFieldForm,
    model_table_view=CustomFieldTableView,
)
