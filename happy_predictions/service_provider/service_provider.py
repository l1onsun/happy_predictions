from dataclasses import dataclass
from typing import Container, Type

from happy_predictions.service_provider.service_factory import ServiceFactories
from happy_predictions.service_provider.types import Service, ServiceClass, TService

_service_locked_sentinel = object()


@dataclass
class ServiceProvider:
    services: dict[ServiceClass, Service]
    factories: ServiceFactories

    def __post_init__(self):
        self.services[ServiceProvider] = self

    def provide(self, service_class: Type[TService]) -> TService:
        try:
            return self._get_service(service_class)
        except KeyError:
            raise RuntimeError(f"Service {service_class} not found")

    def solve(self, service_class: Type[TService]) -> TService:
        try:
            service: Service = self._get_service(service_class)
        except KeyError:
            service = self._build(service_class)
        return service

    def solvable(self) -> Container[ServiceClass]:
        return self.factories.keys() | self.services.keys()

    def solve_all(self):
        for service_class in self.factories:
            self.solve(service_class)

    def _get_service(self, service_class: Type[Service]) -> Service:
        service = self.services[service_class]
        if service is _service_locked_sentinel:
            raise RuntimeError(
                f"Service {service_class} is locked (probably cyclic dependencies)"
            )
        return service

    def _build(self, service_class: Type[Service]) -> Service:
        self.services[service_class] = _service_locked_sentinel
        service: Service = self.factories.get_factory(
            service_class
        ).build_with_provider(self)
        self.services[service_class] = service
        return service
