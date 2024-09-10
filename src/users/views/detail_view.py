import datetime

from common.utils.views import (
    add_notification_headers,
    convert_date_to_readable_string,
    convert_datetime_to_readable_string,
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from users.forms.user import UserCreateForm, UserForm
from users.models import User
from users.services import UserService
from users.views.table_view import USER_TABLE_VIEW

# ------------------------------------------------------------------------------
# Custom UserView
# ------------------------------------------------------------------------------


class UserDetailView:
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
        view_only=False,
        button_text="Add",
        cud_actions_rule=True,
    ):
        self.model = model
        self.model_type = model_type
        self.view_only = view_only
        self.model_name = model_name
        self.model_title = model_name.capitalize().replace("_", " ")
        self.model_service = UserService
        self.model_form = model_form
        self.table_view = model_table_view
        self.model_type = model_type
        self.list_template_name = "users/list.html"
        self.detail_template_name = "users/details.html"
        self.cud_actions_rule = cud_actions_rule
        self.actions_rule = [
            f"view_{model_name.lower()}",
            f"change_{model_name.lower()}",
        ]
        self.button_text = button_text

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
        page_number = request.GET.get("page", 1)

        # Generate table view based on filter and search parameters
        table_rows, paginator, num_pages = self.table_view.table_rows(
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
            "show_actions": True,
            "actions_rule": self.actions_rule,
            "model_name": self.model_name,
            "model_title": self.model_title,
            "view_only": self.view_only,
            "button_text": self.button_text,
            "num_pages": num_pages,
        }

        return render(request, template_name, context)

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
                    if isinstance(getattr(instance, field), datetime.datetime):
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

    def show_create_form(
        self, request, id: int = None, edit: str = "", field: str = ""
    ):
        form_action_url = "/users/create/"

        form = UserCreateForm()
        button_text = "Create"
        view_mode = False
        form_label = "New User Details"
        page_label = "New User"

        context = {
            "form": form,
            "view_mode": view_mode,
            "view_only": self.view_only,
            "form_label": form_label,
            "button_text": button_text,
            "form_action_url": form_action_url,
            "id": id if id else None,
            "page_label": page_label,
            "model_name": self.model_name,
            "model_title": self.model_title,
            "field_url": self.model_name,
            "actions_rule": self.actions_rule,
        }

        if "HX-Request" in request.headers:
            return render(
                request,
                f"{self.list_template_name}#partial-table-template",
                context,
            )

        return render(
            request,
            self.detail_template_name,
            context,
        )

    def show_model_form(self, request, id: int = None, edit: str = "", field: str = ""):
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
        form_action_url = "/users/update/"

        # Process the form based on ID and edit mode
        instance_obj = get_object_or_404(self.model, id=id)
        form = self.model_form(instance=instance_obj)
        if "name" in instance_obj.__dict__:
            page_label = instance_obj.name.capitalize().replace("_", " ")
        else:
            page_label = f"{self.model_title} Details"

        if edit != "true":
            view_mode = True
            form_label = f"{self.model_title} Details"
            button_text = "Edit"
            edit_url = (
                reverse(f"users:edit_{self.model_name.lower()}", args=[id, "true"])
                if self.cud_actions_rule
                else "#"
            )

            # Make all form fields read-only
            for field in form.fields.values():
                field.widget.attrs["disabled"] = True

        else:
            button_text = "Save"
            form_label = f"{self.model_title} Details"
            view_mode = False

        context = {
            "form": form,
            "view_mode": view_mode,
            "view_only": self.view_only,
            "form_label": form_label,
            "button_text": button_text,
            "form_action_url": form_action_url,
            "id": id if id else None,
            "edit_url": edit_url if "edit_url" in locals() else "#",
            "page_label": page_label,
            "model_name": self.model_name,
            "model_title": self.model_title,
            "field_url": self.model_name,
            "actions_rule": self.actions_rule,
        }

        if "HX-Request" in request.headers:
            return render(
                request,
                f"{self.list_template_name}#partial-table-template",
                context,
            )

        return render(
            request,
            self.detail_template_name,
            context,
        )

    # @require_http_methods('POST')
    def create_model_instance(self, request, id: int = None):
        """
        Handle POST request to create or update a model instance using Django form and service.

        Args:
            request: The HTTP request object.
            id: The ID of the model instance (optional).

        Returns:
            The response indicating success or failure of the operation.
        """

        form = UserCreateForm(request.POST)

        if len(form.errors) > 0:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            for error in errors:
                response = HttpResponse(status=400)
                add_notification_headers(response, errors[error][0]["message"], "error")

            return response

        if form.is_valid():
            # Extract data from the form
            obj_data = form.cleaned_data

            # Call the service function to create or update the instance
            UserService(user=request.user).create(**obj_data)
            message = "User created successfully!"

            # Render the form with success message and handle HX-Request
            form = UserCreateForm()

            response = render(
                request,
                f"{self.detail_template_name}#partial-form",
                {
                    "form": form,
                    "button_text": f"Add {self.model_title}",
                    "form_label": f"{self.model_title} Details",
                    "model_name": self.model_name,
                    "model_title": self.model_title,
                    "actions_rule": self.actions_rule,
                },
            )

            if request.htmx:
                headers = {"HX-Redirect": reverse("users:list")}
                response = HttpResponse(status=204, headers=headers)
                add_notification_headers(
                    response,
                    message,
                    "success",
                )
                return response

    def update_model_instance(self, request, id: int = None):
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

        # Get the instance object if updating, otherwise None
        instance_obj = get_object_or_404(self.model, id=id) if id else None

        # Instantiate the form with POST data and optionally the instance object
        form = self.model_form(request.POST, instance=instance_obj)

        if len(form.errors) > 0:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            for error in errors:
                response = HttpResponse(status=400)
                add_notification_headers(response, errors[error][0]["message"], "error")

            return response

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
                message = f"{self.model_title} updated successfully!"

            except self.model.DoesNotExist:
                response = HttpResponse(status=404)
                add_notification_headers(
                    response, errors[error][0]["message"], "User not found"
                )
                return response

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
                    "actions_rule": self.actions_rule,
                    "id": obj_data["id"],
                },
            )

            if request.htmx:
                headers = {"HX-Redirect": reverse("users:list")}
                response = HttpResponse(status=204, headers=headers)
                add_notification_headers(
                    response,
                    message,
                    "success",
                )
                return response


USER_VIEWS = UserDetailView(
    model=User,
    model_name="users",
    model_service=UserService,
    model_form=UserForm,
    model_table_view=USER_TABLE_VIEW,
)
