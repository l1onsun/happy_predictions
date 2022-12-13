from typing import Type

from fastapi import Depends, Request

from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.service_provider.types import Service, TService


def get_service_provider(request: Request) -> ServiceProvider:
    return request.app.service_provider


def provide(service_class: Type[TService]) -> TService:
    def fastapi_dependency(
        service_provider: ServiceProvider = Depends(get_service_provider),
    ) -> Service:
        return service_provider.provide(service_class)

    return Depends(fastapi_dependency)
