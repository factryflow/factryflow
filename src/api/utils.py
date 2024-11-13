from http import HTTPStatus
from django.core.exceptions import FieldDoesNotExist
from typing import List

from django.db import models, IntegrityError
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
            self.path,
            response={HTTPStatus.CREATED: self.output_schema},
            summary=f"Create {self.name}",
            operation_id=f"{self.name}_create",
        )
        def create(request: HttpRequest, payload: self.input_schema):
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
        for field_name, field_value in payload_data.items():
            try:
                field = self.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                continue

            if isinstance(field, models.ForeignKey):
                related_model = field.remote_field.model
                try:
                    related_instance = get_object_or_404(related_model, id=field_value)
                except Http404:
                    raise Http404(
                        f"{related_model.__name__} with id {field_value} not found"
                    )
                payload_data[field_name] = related_instance

        return payload_data
