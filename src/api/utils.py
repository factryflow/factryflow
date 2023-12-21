from http import HTTPStatus
from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router


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

    def get_instance(self, id: int):
        return get_object_or_404(self.model, id=id)

    def define_routes(self):
        # CREATE
        @self.router.post(
            self.path,
            response={HTTPStatus.CREATED: self.output_schema},
            summary=f"Create {self.name}",
        )
        def create(request: HttpRequest, payload: self.input_schema):
            instance = self.service().create(**payload.model_dump())
            return instance

        # LIST
        @self.router.get(
            self.path,
            response={HTTPStatus.OK: List[self.output_schema]},
            summary=f"List {self.name_plural}",
        )
        def list(request: HttpRequest):
            instances = self.model.objects.all()
            return instances

        # RETRIEVE
        @self.router.get(
            self.path + "/{id}",
            response={HTTPStatus.OK: self.output_schema},
            summary=f"Retrieve {self.name}",
        )
        def get(request: HttpRequest, id: int):
            instance = self.get_instance(id=id)
            return instance

        # UPDATE
        @self.router.put(
            self.path + "/{id}",
            response={HTTPStatus.OK: self.output_schema},
            summary=f"Update {self.name}",
        )
        def update(request: HttpRequest, id: int, payload: self.input_schema):
            instance = self.get_instance(id=id)
            instance = self.service().update(
                instance=instance, data=payload.model_dump()
            )
            return instance

        # DELETE
        @self.router.delete(
            self.path + "/{id}",
            response={HTTPStatus.NO_CONTENT: None},
            summary=f"Delete {self.name}",
        )
        def delete(request: HttpRequest, id: int):
            instance = self.get_instance(id=id)
            self.service().delete(instance=instance)
            return None