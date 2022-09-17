from types import FunctionType
from typing import Callable

import telegram.ext as tge

from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.services.telegram.provided_handlers_types import (
    CallbackQueryHandlerResolver,
    CommandHandlerResolver,
    ProvidedHandler,
)


def _add_handler_to_handlers_list(
    method: Callable[["ProvidedHandlers", FunctionType], ProvidedHandler]
):
    def converted(self: "ProvidedHandlers", callback: FunctionType):
        self.handlers_list.append(method(self, callback))
        return callback

    return converted


class ProvidedHandlers:
    def __init__(self):
        self.handlers_list: list[ProvidedHandler] = []

    def resolve(self, service_provider: ServiceProvider) -> list[tge.BaseHandler]:
        return [handler.solve(service_provider) for handler in self.handlers_list]

    @_add_handler_to_handlers_list
    def add_start_handler(self, callback: FunctionType):
        return CommandHandlerResolver("start", callback)

    @_add_handler_to_handlers_list
    def add_callback_query_handler(self, callback: FunctionType):
        return CallbackQueryHandlerResolver(callback)
