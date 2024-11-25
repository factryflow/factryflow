from http import HTTPStatus
from typing import List

from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError, models
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import Http404

from api.schemas import DeleteResponseSchema


class CRUDModelViewSet:
    def __init__(
        self, *, model, service, input_schema, output_schema, path=None, **router_kwargs
    ):
        self.router = Router(**router_kwargs)
        self.model = model
        self.service = service
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.name = model.__name__.lower()
        self.name_plural = model._meta.verbose_name_plural.lower()
        self.path = path or f"/{self.name_plural}"
        self.define_routes()

    def define_routes(self):
        # CREATE
        @self.router.post(
            # Endpoint to create a new instance
            self.path,
            response={HTTPStatus.CREATED: self.output_schema},
            summary=f"Create {self.name}",
            operation_id=f"{self.name}_create",
        )
        def create(request: HttpRequest, payload: self.input_schema):
            """
            Create a new instance using the provided request and payload.

            Args:
                request (HttpRequest): The HTTP request object containing user information.
                payload (self.input_schema): The input schema containing the data to be processed.

            Returns:
                instance: The created instance after processing the payload and saving it using the service.

            Raises:
                ValidationError: If the payload data is invalid.
                PermissionDenied: If the user does not have permission to create the instance.

            """
            data = self._process_foreign_keys(payload_data=payload.model_dump())
            instance = self.service(user=request.user).create(**data)
            return instance

        # LIST
        @self.router.get(
            self.path,
            response={HTTPStatus.OK: List[self.output_schema]},
            summary=f"List {self.name_plural}",
            operation_id=f"{self.name}_list",
        )
        def list(request: HttpRequest):
            """
            Retrieve a list of all instances of the model.

            Args:
                request (HttpRequest): The HTTP request object.

            Returns:
                QuerySet: A QuerySet containing all instances of the model.
            """
            instances = self.model.objects.all()
            return instances

        # RETRIEVE
        @self.router.get(
            self.path + "/{id}",
            response={HTTPStatus.OK: self.output_schema},
            summary=f"Retrieve {self.name}",
            operation_id=f"{self.name}_retrieve",
        )
        def get(request: HttpRequest, id: int):
            """
            Retrieve a single instance of the model by its ID.

            Args:
                request (HttpRequest): The HTTP request object.
                id (int): The ID of the instance to retrieve.

            Returns:
                instance: The retrieved instance of the model.

            Raises:
                Http404: If the instance with the given ID does not exist.
            """
            instance = self._get_instance(id=id)
            return instance

        # UPDATE
        @self.router.put(
            self.path + "/{id}",
            response={HTTPStatus.OK: self.output_schema},
            summary=f"Update {self.name}",
            operation_id=f"{self.name}_update",
        )
        def update(request: HttpRequest, id: int, payload: self.input_schema):
            """
            Updates an instance with the given payload data.

            Args:
                request (HttpRequest): The HTTP request object containing user information.
                id (int): The unique identifier of the instance to be updated.
                payload (self.input_schema): The data schema containing the updated information.

            Returns:
                instance: The updated instance.

            Raises:
                Http404: If the instance with the given id does not exist.
                ValidationError: If the payload data is invalid.

            """
            instance = self._get_instance(id=id)
            data = self._process_foreign_keys(payload_data=payload.model_dump())
            instance = self.service(user=request.user).update(instance, data)
            return instance

        # DELETE
        @self.router.delete(
            self.path + "/{id}",
            response=DeleteResponseSchema,
            summary=f"Delete {self.name}",
            operation_id=f"{self.name}_delete",
        )
        def delete(request: HttpRequest, id: int):
            """
            Deletes an instance of the model with the given ID.

            Args:
                request (HttpRequest): The HTTP request object containing user information.
                id (int): The ID of the instance to be deleted.

            Returns:
                dict: A dictionary containing the status and message of the delete operation.
                    - "status" (HTTPStatus): The HTTP status code indicating the result of the operation.
                    - "message" (str): A message describing the result of the operation.

            Raises:
                IntegrityError: If the instance cannot be deleted due to a foreign key constraint.
            """
            instance = self._get_instance(id=id)
            try:
                self.service(user=request.user).delete(instance)
                return {
                    "status": HTTPStatus.OK,
                    "message": f"{self.model.__name__} with id {id} deleted successfully",
                }
            except IntegrityError:
                return {
                    "status": HTTPStatus.BAD_REQUEST,
                    "message": f"Cannot delete {self.model.__name__} with id {id} due to foreign key constraint",
                }

    def _get_instance(self, id: int):
        try:
            return get_object_or_404(self.model, id=id)
        except Http404:
            raise Http404(f"{self.model.__name__} with id {id} not found")

    def _process_foreign_keys(self, payload_data):
        """
        Processes the foreign key and many-to-many fields in the given payload data.

        This method iterates over the items in the payload data and checks if the field
        is a ForeignKey or ManyToManyField. If it is, it processes the field accordingly
        and updates the payload data with the processed values.

        Args:
            payload_data (dict): The payload data containing field names and values.

        Returns:
            dict: The updated payload data with processed foreign key and many-to-many fields.
        """
        for field_name, field_value in payload_data.items():
            try:
                field = self.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                continue

            if isinstance(field, models.ForeignKey):
                payload_data[field_name] = self._process_foreign_key_field(
                    field, field_value
                )
            elif isinstance(field, models.ManyToManyField):
                payload_data[field_name] = self._process_many_to_many_field(
                    field, field_value
                )

        return payload_data

    def _process_foreign_key_field(self, field, field_value):
        """
        Processes a foreign key field and retrieves the related instance.

        Args:
            field (models.Field): The foreign key field to process.
            field_value (int or None): The value of the foreign key field. If None or 0, returns None.

        Returns:
            models.Model or None: The related model instance if found, otherwise raises Http404 with a message.
        """
        if field_value is None or field_value == 0:
            return None
        related_model = field.remote_field.model
        try:
            related_instance = get_object_or_404(related_model, id=field_value)
            return related_instance
        except Http404:
            raise Http404(f"{related_model.__name__} with id {field_value} not found")

    def _process_many_to_many_field(self, field, field_value):
        """
        Processes a many-to-many field and retrieves related model instances.

        Args:
            field (django.db.models.fields.related.ManyToManyField): The many-to-many field to process.
            field_value (list): A list of related model instance IDs.

        Returns:
            list: A list of related model instances. If field_value is empty, returns an empty list.
        """
        if not field_value:
            return []
        related_model = field.remote_field.model
        related_instances = []
        for related_id in field_value:
            if related_id:
                try:
                    related_instance = get_object_or_404(related_model, id=related_id)
                    related_instances.append(related_instance)
                except Http404:
                    raise Http404(
                        f"{related_model.__name__} with id {related_id} not found"
                    )
        return related_instances
