from types import FunctionType

from fastapi import Depends, Request

from happy_predictions.service_provider.partial_function_resolve import (
    partial_function_resolve,
)
from happy_predictions.service_provider.service_factory import ServiceFactories
from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.service_provider.types import Service, ServiceClass


def get_service_provider(request: Request) -> ServiceProvider:
    return request.app.service_provider


def provide(service_class: ServiceClass) -> Service:
    def fastapi_dependency(
        service_provider: ServiceProvider = Depends(get_service_provider),
    ) -> Service:
        return service_provider.provide(service_class)

    return Depends(fastapi_dependency)


def provide_fastapi_dependencies(factories: ServiceFactories):
    def decorator(endpoint: FunctionType):
        return partial_function_resolve(
            endpoint,
            services_to_resolve=factories.keys(),
            resolve_by_callable=provide,
        )

    return decorator
