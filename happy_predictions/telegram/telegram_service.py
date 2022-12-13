from dataclasses import InitVar, dataclass

import telegram.ext as tge

from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.telegram.fix_telegram_types import Update
from happy_predictions.telegram.provided_handlers import ProvidedHandlers
from happy_predictions.utils import JsonType


@dataclass
class TelegramService:
    service_provider: ServiceProvider
    application: tge.Application
    handlers: InitVar[ProvidedHandlers]

    def __post_init__(self, handlers: ProvidedHandlers):
        self.application.add_handlers(handlers.resolve(self.service_provider))

    def parse_update_from_json(self, json: JsonType) -> Update:
        return Update.de_json(json, self.application.bot)

    async def process_update(self, update: Update):
        return await self.application.process_update(update)

    async def initialize(self, webhook_url: str):
        await self.application.initialize()
        await self.application.bot.set_webhook(webhook_url)

    async def shutdown(self):
        return await self.application.shutdown()
