import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from common.utils.views import add_notification_headers, convert_datetime_to_readable_string,   convert_date_to_readable_string


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
        model_type=None,
    ):
        self.model = model
        self.model_type = model_type
        self.model_name = model_name
        self.model_service = model_service
        self.model_form = model_form
        self.table_view = model_table_view
        self.model_type = model_type
        self.list_template_name = "objects/list.html"
        self.detail_template_name = "objects/details.html"
        self.actions_rule = [
            f"view_{model_name.lower()}",
            f"add_{model_name.lower()}",
            f"change_{model_name.lower()}",
            f"delete_{model_name.lower()}",
        ]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Dispatches the request to the appropriate view method.
        return super().dispatch(request, *args, **kwargs)

    def get_all_instances(self, request):
        """
        View function to display all instances with optional filtering.

        Returns:
            The rendered response displaying all instances.
        """
        # Retrieve filtering and search parameters from the request
        status_filter = request.GET.get("status", "all")
        search_query = request.GET.get("query", "")

        # Generate table view based on filter and search parameters
        table_rows = self.table_view.table_rows(
            status_filter=status_filter, search_query=search_query
        )

        template_name = self.list_template_name

        # Determine whether to include partial template based on request headers
        if "HX-Request" in request.headers:
            template_name += "#partial-table-template"

        context = {
            "headers": self.table_view.table_headers,
            "status_filter_dict": self.table_view.status_filter_dict,
            "rows": table_rows,
            "show_actions": True,
            "actions_rule": self.actions_rule,
            "model_name": self.model_name,
        }

        return render(request, template_name, context)

    def show_model_form(self, request, id: int = None, edit: str = ""):
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
        form_action_url = f"/{self.model_name.lower()}-create/"

        # Process the form based on ID and edit mode
        if id:
            instance_obj = get_object_or_404(self.model, id=id)
            form = self.model_form(instance=instance_obj)
            page_label = instance_obj.name

            if edit != "true":
                view_mode = True
                form_label = f"{self.model_name.capitalize()} Details"
                button_text = "Edit"
                edit_url = reverse(f"edit_{self.model_name.lower()}", args=[id, "true"])

                # Make all form fields read-only
                for field in form.fields.values():
                    field.widget.attrs["readonly"] = True

            else:
                button_text = "Save"
                form_label = f"{self.model_name.capitalize()} Details"
                view_mode = False

        else:
            form = self.model_form()
            button_text = "Create"
            view_mode = False
            form_label = f"New {self.model_name.capitalize()} Details"
            page_label = f"New {self.model_name.capitalize()}"

        context = {
            "form": form,
            "view_mode": view_mode,
            "form_label": form_label,
            "button_text": button_text,
            "form_action_url": form_action_url,
            "id": id if id else None,
            "edit_url": edit_url if "edit_url" in locals() else "#",
            "page_label": page_label,
            "model_name": self.model_name,
            "actions_rule": self.actions_rule,
        }

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
        # Get the instance object if updating, otherwise None
        instance_obj = get_object_or_404(self.model, id=id) if id else None

        # Instantiate the form with POST data and optionally the instance object
        form = self.model_form(request.POST, instance=instance_obj)
        id = request.POST.get("id")

        if form.is_valid():
            # Extract data from the form
            obj_data = form.cleaned_data

            # Call the service function to create or update the instance
            obj_data["id"] = id
            try:
                existing_instance = self.model.objects.get(id=obj_data["id"])
                self.model_service(user=request.user).update(
                    existing_instance, obj_data
                )

            except self.model.DoesNotExist:
                del obj_data["id"]
                self.model_service(user=request.user).create(**obj_data)

            # Render the form with success message and handle HX-Request
            form = self.model_form()
            response = render(
                request,
                f"{self.detail_template_name}#partial-form",
                {
                    "form": form,
                    "button_text": f"Add {self.model_name.capitalize()}",
                    "form_label": f"{self.model_name.capitalize()} Details",
                    "model_name": self.model_name,
                    "actions_rule": self.actions_rule,
                },
            )

            if request.htmx:
                headers = {"HX-Redirect": reverse(f"{self.model_name.lower()}")}
                response = HttpResponse(status=204, headers=headers)
                add_notification_headers(
                    response,
                    f"{self.model_name.capitalize()} created successfully!",
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

        # Generate table view based on filter and search parameters
        table_rows = self.table_view.table_rows(
            status_filter=status_filter, search_query=search_query
        )

        # Render the updated table and add notification headers
        response = render(
            request,
            f"{self.list_template_name}#partial-table-template",
            {
                "headers": self.table_view.table_headers,
                "status_filter_dict": self.table_view.status_filter_dict,
                "rows": table_rows,
                "show_actions": True,
                "actions_rule": self.actions_rule,
                "model_name": self.model_name,
            },
        )

        # Add notification based on deletion success or failure
        if deletion_successful:
            add_notification_headers(
                response, f"{self.model_name.capitalize()} has been deleted.", "info"
            )
        else:
            add_notification_headers(
                response,
                f"Failed to delete the {self.model_name.capitalize()}.",
                "error",
            )

        return response


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
        status_choices_class=None,
        status_filter_field=None,
        tailwind_classes=None,
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
        self.status_filter_dict = status_choices_class.to_dict() if status_choices_class else {}
        self.tailwind_classes = tailwind_classes
        self.fields = fields
        self.table_headers = headers

    @property
    def all_instances(self):
        """
        Retrieve all instances of the model.
        """
        return self.model.objects.all()

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

    def table_rows(
        self,
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
        rows = []
        for instance in self.filtered_instances(status_filter, search_query):
            row_data = []
            for field in self.fields:
                if "status" in field:
                    value = (
                        f'<span class="{self.get_status_colored_text(getattr(instance, field))} text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">'
                        f'{getattr(instance, "get_" + self.model_name + "_status_display")()}</span>',
                    )
                    row_data.append(value[0])
                
                # if value is datetime instance convert to readable format
                elif isinstance(getattr(instance, field), datetime.datetime):
                    value = convert_datetime_to_readable_string(
                        getattr(instance, field)
                    )
                    row_data.append(value)

                # if value is date instance convert to readable format
                elif isinstance(getattr(instance, field), datetime.date):
                    value = convert_date_to_readable_string(getattr(instance, field))
                    row_data.append(value)

                else:
                    value = getattr(instance, field)
                    # if callable(value):
                    #     value = value()
                    row_data.append(value)
            rows.append(row_data)
        return rows

    def get_status_colored_text(self, model_status):
        """
        Get the colored text based on model status.

        Args:
            model_status: The status of the model.

        Returns:
            str: The Tailwind CSS class for the given model status.
        """
        return self.tailwind_classes.get(model_status)
