import inspect
from types import FunctionType
from typing import Any

import telegram.ext as tge
from telegram._update import Update
from telegram.ext._utils.types import HandlerCallback

from happy_predictions.service_provider.partial_function_resolve import (
    partial_function_resolve,
)
from happy_predictions.service_provider.service_provider import ServiceProvider


def resolve_callback(
    unresolved_callback: FunctionType, service_solver: ServiceProvider
) -> HandlerCallback:
    resolved_callback = partial_function_resolve(
        unresolved_callback, service_solver.solvable(), service_solver.solve
    )
    update_param_name, context_param_name = get_update_and_context_param_names(
        resolved_callback
    )

    async def tg_handler_callback(update: Update, context: tge.CallbackContext):
        kwargs: dict[str, Any] = {}
        if update_param_name:
            kwargs[update_param_name] = update
        if context_param_name:
            kwargs[context_param_name] = context
        await resolved_callback(**kwargs)

    return tg_handler_callback


def get_update_and_context_param_names(
    callback: FunctionType,
) -> tuple[str | None, str | None]:
    update_param_name = None
    context_param_name = None
    for param in inspect.signature(callback).parameters.values():
        if param.annotation is Update:
            update_param_name = param.name
        elif param.annotation is tge.CallbackContext:
            context_param_name = param.name

    return update_param_name, context_param_name
