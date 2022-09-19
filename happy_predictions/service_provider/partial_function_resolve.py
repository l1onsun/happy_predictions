import functools
import inspect
from typing import Any, Callable, Container

from happy_predictions.service_provider.types import ServiceClass


def partial_function_resolve(
    function: Callable,
    services_to_resolve: Container[ServiceClass],
    resolve_by_callable: Callable[[ServiceClass], Any],
):
    partial_kwargs = {}
    for parameter in inspect.signature(function).parameters.values():
        if parameter.annotation in services_to_resolve:
            partial_kwargs[parameter.name] = resolve_by_callable(parameter.annotation)

    return functools.partial(function, **partial_kwargs)
