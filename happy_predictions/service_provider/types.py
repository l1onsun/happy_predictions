from typing import Callable, Type, TypeVar

Service = TypeVar("Service")
ServiceClass = Type[Service]
BuilderFunc = Callable
