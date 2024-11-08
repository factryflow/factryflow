from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.utils import IntegrityError
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from common.models import CustomField
from common.utils.views import (
    add_notification_headers,
)

# ------------------------------------------------------------------------------
# Custom CRUDView
# ------------------------------------------------------------------------------


class CRUDView:
    """
    A generic CRUD (Create, Read, Update, Delete) view for handling various models.
    """

    def __init__(
        self,
        model,
        model_name,
        model_service,
        model_form,
        model_table_view,
        formset_options=[],
        inline_formset=[],
        model_type=None,
        view_only=False,
        sub_model_relation=False,
        button_text="Add",
        ordered_model=False,
        user_rule_permission=True,
    ):
        """
        Attributes:
            model: The model class.
            model_type: The type of model (optional).
            model_name: The name of the model.
            model_service: The service class handling model operations.
            model_form: The form class for the model.
            table_view: The view class for rendering model data in a tabular format.
            list_template_name: The name of the template for listing model instances.
            detail_template_name: The name of the template for displaying model details.
            user_rule_permission: Flag indicating if user has permission for CRUD actions.
            crud_action_rules: List of CRUD permissions for the model.
            button_text: Text for the action button.
            ordered_model: Flag indicating if the model is ordered.
            formset_options: Options for inline formsets.
            model_formset: Inline formset for the model.
            sub_model_relation: Flag indicating if the model has sub-model relations.
        """
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
        self.crud_action_rules = self.get_models_crud_permissions(
            self.model._meta.model_name
        )
        self.button_text = button_text
        self.ordered_model = ordered_model
        self.formset_options = formset_options
        self.inline_formset = inline_formset
        self.model_formset = None
        self.model_inline_formset = None
        self.sub_model_relation = sub_model_relation
        self.num_of_rows_per_page = 25
        self.sort_direction = "asc"
        self.sort_by = "id"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Dispatches the request to the appropriate view method.
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def check_change_password(user):
        """
        Check if the user is required to change their password.

        Args:
            user: The user object.

        Returns:
            True if the user is required to change their password, False otherwise.
        """
        if user.require_password_change:
            return True
        return False

    def get_models_crud_permissions(self, model_name):
        """
        Get the CRUD permissions for a given model.

        Args:
            model_name: The name of the model.

        Returns:
            A list of CRUD permissions for the model.
        """
        permissions_list = (
            [
                f"view_{model_name.lower().replace('_', '')}",
                f"add_{model_name.lower().replace('_', '')}",
                f"change_{model_name.lower().replace('_', '')}",
                f"delete_{model_name.lower().replace('_', '')}",
            ]
            if model_name
            else None
        )
        return permissions_list

    def get_custom_field_json_data(self, content_type, instance=None):
        """
        Retrieve custom field data in JSON format for a given content type and instance.

        Args:
            content_type: The content type of the model.
            instance: The model instance (optional).

        Returns:
            A list of dictionaries containing custom field data.
        """
        data = []

        # Get custom fields from the instance if available, otherwise get default custom fields
        custom_fields = (
            instance.custom_fields
            if instance and instance.custom_fields != {}
            else {
                field.name: ""
                for field in CustomField.objects.filter(content_type=content_type)
            }
        )

        # Iterate over custom fields and construct the data list
        for id, (key, value) in enumerate(custom_fields.items(), start=1):
            custom_field_instance = CustomField.objects.get(
                name=key, content_type=content_type
            )
            data.append(
                {
                    "id": id,
                    "name": custom_field_instance.name,
                    "label": custom_field_instance.label,
                    "type": custom_field_instance.field_type,
                    "value": value,
                    "is_required": custom_field_instance.is_required,
                }
            )

        return data

    def get_all_instances(self, request):
        """
        View function to display all instances with optional filtering.

        Args:
            request: The HTTP request object.

        Returns:
            The rendered response displaying all instances.
        """

        if self.check_change_password(request.user):
            return redirect(reverse("users:change_password"))

        # Retrieve filtering and search parameters from the request
        status_filter = request.GET.get("status", "all")
        search_query = request.GET.get("query", "")
        page_number = request.GET.get("page", 1)
        self.num_of_rows_per_page = request.GET.get(
            "num_of_rows_per_page", self.num_of_rows_per_page
        )
        self.sort_direction = request.GET.get("sort_direction", self.sort_direction)
        self.sort_by = request.GET.get("sort_by", self.sort_by)

        # Generate table view based on filter and search parameters
        table_rows, paginator, num_pages, total_instances_count = (
            self.table_view.table_rows(
                status_filter=status_filter,
                search_query=search_query,
                page_number=page_number,
                sort_direction=self.sort_direction,
                sort_field=self.sort_by,
                num_of_rows_per_page=self.num_of_rows_per_page,
            )
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
            "num_pages": num_pages,
            "num_of_rows_per_page": self.num_of_rows_per_page,
            "total_instances_count": total_instances_count,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
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
        Display a form for creating or editing a model instance.

        Args:
            request: The HTTP request object.
            id: The ID of the model instance (optional).
            edit: Flag indicating whether the form is in edit mode (optional).
            field: The field name for relation (optional).
            formset_count: The number of forms in the formset (optional).

        Returns:
            The rendered response displaying the model form.
        """
        if self.check_change_password(request.user):
            return redirect(reverse("users:change_password"))

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
            formset_model_name = self.formset_options[-1]

            formset_action_url = (
                f"/{formset_model_name.replace('_', '-').lower()}-create/"
            )

        if len(self.inline_formset) > 0:
            self.model_inline_formset = inlineformset_factory(
                self.model,
                self.inline_formset[0],
                form=self.inline_formset[1],
                extra=1,
                can_delete=True,
            )

            inline_formset_model_name = self.inline_formset[-1]

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

        # get relation table headers
        relation_table_headers = (
            ["ID", "Name", "Label", "Type", "Value"]
            if relation_field_name == "custom_fields"
            else self.table_view.model_relation_fields[relation_field_name].get(
                "headers"
            )
        )

        # get relation field names
        if relation_field_name != "custom_fields":
            relationship_fields = self.table_view.model_relation_fields[
                relation_field_name
            ].get("relationship_fields")
            if relationship_fields:
                model_relation_field_name = relationship_fields

        # to show edit actions for model relation table
        show_edit_actions = (
            False
            if relation_field_name == "custom_fields"
            else self.table_view.model_relation_fields[relation_field_name].get(
                "show_edit_actions"
            )
        )

        # model name of relation field
        relation_model_name = (
            self.table_view.model_relation_fields[relation_field_name].get("model_name")
            if relation_field_name not in ["custom_fields", "history"]
            else relation_field_name
        )

        # add and remove urls for formset
        if len(self.formset_options) > 0:
            add_formset_url = (
                reverse(
                    f"{self.model_name.lower()}_formset",
                    kwargs={"formset_count": formset_count + 1},
                )
                if self.user_rule_permission
                else None
            )

            remove_formset_url = (
                reverse(
                    f"{self.model_name.lower()}_formset",
                    kwargs={
                        "formset_count": formset_count - 1 if formset_count > 0 else 0
                    },
                )
                if self.user_rule_permission
                else None
            )

        context = {
            "form": form,
            "formset_title": self.formset_options[2] if self.formset_options else None,
            "formset_form": (
                self.model_formset(instance=instance_obj)
                if id
                else self.model_formset()
            )
            if self.model_formset
            else None,
            "formset_action_url": formset_action_url if self.model_formset else None,
            "add_formset_url": add_formset_url
            if "add_formset_url" in locals()
            else None,
            "remove_formset_url": remove_formset_url
            if "remove_formset_url" in locals()
            else None,
            "inline_formset_form": (
                self.model_inline_formset(instance=instance_obj)
                if id
                else self.model_inline_formset()
            )
            if self.model_inline_formset
            else None,
            "inline_formset_title": inline_formset_model_name.replace("_", " ").title()
            if self.model_inline_formset
            else None,
            "show_edit_actions": show_edit_actions,
            "model_relation_field_name": model_relation_field_name
            if "model_relation_field_name" in locals()
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
            "crud_action_rules": self.crud_action_rules,
            "relation_model_crud_action_rules": self.get_models_crud_permissions(
                relation_model_name
            ),
            "model_title": self.model_title,
            "field_url": self.model_name.replace("_", "-").lower(),
            "custom_field_data": custom_field_form_data
            if custom_field_form_data
            else None,
            "show_actions": True if edit == "true" and relation_model_name else False,
            "headers": relation_table_headers if relation_field_name else [],
            "relations_headers": self.table_view.model_relation_headers,
            "rows": rows if rows != [] else None,
            "relation_model_name": relation_model_name.replace("_", " ").title(),
        }

        if "HX-Request" in request.headers:
            # if formset_count in the request as path parameters then return details page with #new-row-formset
            if "field" in str(request.path):
                return render(
                    request,
                    f"{self.detail_template_name}#model-relation-editable-table",
                    context,
                )

            if "formset" in str(request.path):
                return render(
                    request,
                    f"{self.detail_template_name}#inline-model-form",
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

        custom_fields_keys = CustomField.objects.filter(
            content_type=ContentType.objects.get_for_model(self.model)
        ).values_list("name", flat=True)
        custom_fields_values = [request.POST.get(key) for key in custom_fields_keys]

        custom_fields_data = dict(zip(custom_fields_keys, custom_fields_values))

        # Get the instance object if updating, otherwise None
        instance_obj = get_object_or_404(self.model, id=id) if id else None

        # Initiate the form with POST data and optionally the instance object
        form = self.model_form(
            request.POST, instance=instance_obj if instance_obj else None
        )

        model_inline_form = (
            self.model_inline_formset(
                request.POST, instance=instance_obj if instance_obj else None
            )
            if self.model_inline_formset
            else None
        )

        # form validation
        model_inline_form_errors_len = (
            len(model_inline_form.errors) if model_inline_form else 0
        )

        if len(form.errors) > 0 or model_inline_form_errors_len > 0:
            errors_list = (
                list(form.errors.items()) + list(model_inline_form.errors[0].items())
                if self.model_inline_formset
                else list(form.errors.items())
            )

            errors = {f: e.get_json_data() for f, e in errors_list}
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

            # add data from model_inline_formset data
            if (
                model_inline_form
                and model_inline_form.is_valid()
                and model_inline_form.cleaned_data != [{}]
            ):
                obj_data[self.inline_formset[2]] = model_inline_form.cleaned_data

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
                headers = None
                if not self.sub_model_relation:
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

        try:
            # Delete the instance and check if deletion was successful
            with transaction.atomic():
                deletion_successful = self.model_service(user=request.user).delete(obj)
        except IntegrityError:
            deletion_successful = False

        # Retrieve updated instance list
        status_filter = request.GET.get("status", "all")
        search_query = request.GET.get("query", "")
        page_number = request.GET.get("page", 1)
        self.sort_by = request.GET.get("sort_by", self.sort_by)
        self.num_of_rows_per_page = request.GET.get(
            "num_of_rows_per_page", self.num_of_rows_per_page
        )
        self.sort_direction = request.GET.get("sort_direction", self.sort_direction)
        self.sort_by = request.GET.get("sort_by", self.sort_by)

        # Generate table view based on filter and search parameters
        table_rows, paginator, num_pages, total_instances_count = (
            self.table_view.table_rows(
                status_filter=status_filter,
                search_query=search_query,
                page_number=page_number,
                sort_by=self.sort_by,
                sort_direction=self.sort_direction,
                sort_field=self.sort_by,
                num_of_rows_per_page=self.num_of_rows_per_page,
            )
        )

        # template name based on is_redirect variable
        template_name = (
            f"{self.detail_template_name}#model-relation-editable-table"
            if self.sub_model_relation
            else f"{self.list_template_name}#partial-table-template"
        )

        # Render the updated table and add notification headers
        response = render(
            request,
            template_name,
            {
                "headers": self.table_view.table_headers,
                "status_filter_dict": self.table_view.status_filter_dict,
                "rows": table_rows,
                "num_pages": num_pages,
                "total_instances_count": total_instances_count,
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

        if request.htmx and deletion_successful and self.sub_model_relation:
            response = HttpResponse(status=204)
            add_notification_headers(
                response,
                f"{self.model_title} has been deleted.",
                "success",
            )
            return response

        return response
