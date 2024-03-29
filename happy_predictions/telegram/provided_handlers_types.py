from dataclasses import dataclass
from typing import Callable, Protocol

import telegram.ext as tge

from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.telegram.resolve_handler_callback import resolve_callback


class ProvidedHandler(Protocol):
    def solve(self, service_provider: ServiceProvider) -> tge.BaseHandler:
        ...


@dataclass
class CommandHandlerResolver(ProvidedHandler):
    command: str
    unresolved_callback: Callable

    def solve(self, service_provider: ServiceProvider):
        return tge.CommandHandler(
            self.command, resolve_callback(self.unresolved_callback, service_provider)
        )


@dataclass
class CallbackQueryHandlerResolver(ProvidedHandler):
    unresolved_callback: Callable

    def solve(self, service_provider: ServiceProvider):
        return tge.CallbackQueryHandler(
            resolve_callback(self.unresolved_callback, service_provider)
        )


@dataclass
class MessageHandlerResolver(ProvidedHandler):
    unresolved_callback: Callable

    def solve(self, service_provider: ServiceProvider):
        return tge.MessageHandler(
            tge.filters.ALL,
            resolve_callback(self.unresolved_callback, service_provider),
        )
