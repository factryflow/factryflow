from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.db import transaction

from common.utils.views import add_notification_headers


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
    def __init__(self, model, model_name, model_service, model_form, model_table_view, model_type = None):
        self.model = model
        self.model_type = model_type
        self.model_name = model_name
        self.model_service = model_service
        self.model_form = model_form
        self.table_view = model_table_view
        self.model_type = model_type
        self.list_template_name = "objects/list.html"
        self.detail_template_name = "objects/details.html"

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
        table = self.table_view(status_filter=status_filter, search_query=search_query)

        template_name = self.list_template_name

        # Determine whether to include partial template based on request headers
        if "HX-Request" in request.headers:
            template_name += "#partial-table-template"

        context = {
            "headers": table.table_headers,
            "rows": table.table_rows,
            "show_actions": True,
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
                updated_instance = self.model_service(user=request.user).update(existing_instance, obj_data)
            
            except self.model.DoesNotExist:
                del obj_data["id"]
                new_instance = self.model_service(user=request.user).create(**obj_data)

            # Render the form with success message and handle HX-Request
            form = self.model_form()
            response = render(
                request,
                f"{self.detail_template_name}#partial-form",
                {"form": form, "button_text": f"Add {self.model_name.capitalize()}", "form_label": f"{self.model_name.capitalize()} Details"},
            )

            if request.htmx:
                headers = {
                    "HX-Redirect": reverse(
                        f"{self.model_name.lower()}"
                    )
                }
                response = HttpResponse(status=204, headers=headers)
                add_notification_headers(response, f"{self.model_name.capitalize()} created successfully!", "success")
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
        table = self.table_View(status_filter=status_filter)

        # Render the updated table and add notification headers
        response = render(
            request,
            f"{self.list_template_name}#partial-table-template",
            {
                "headers": table.table_headers,
                "rows": table.table_rows,
                "show_actions": True,
            },
        )

        # Add notification based on deletion success or failure
        if deletion_successful:
            add_notification_headers(response, f"{self.model_name.capitalize()} has been deleted.", "info")
        else:
            add_notification_headers(response, f"Failed to delete the {self.model_name.capitalize()}.", "error")

        return response
