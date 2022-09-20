from typing import NewType

import telegram.ext as tge
from fastapi import FastAPI
from telegram import Bot

from happy_predictions.const import TELEGRAM_WEBHOOK_PATH
from happy_predictions.env import Env
from happy_predictions.predictor.assets_manager import AssetsBox
from happy_predictions.predictor.image_generation import ImageGenerator
from happy_predictions.predictor.predictor import Predictor
from happy_predictions.service_provider.service_factory import ServiceFactories
from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.storage.mongo_storage.mongo_storage import MongoStorage
from happy_predictions.storage.storage import Storage
from happy_predictions.telegram.telegram_service import TelegramService
from happy_predictions.telegram_handlers import telegram_handlers
from happy_predictions.telegram_webhook import router as telegram_webhook_router
from happy_predictions.utils import url_join

service_factories = ServiceFactories()

WebhookFullUrl = NewType("WebhookFullUrl", str)


@service_factories.add
def build_fastapi(
    service_provider: ServiceProvider, webhook_url: WebhookFullUrl
) -> FastAPI:
    async def on_startup():
        service_provider.solve_all()
        telegram = service_provider.provide(TelegramService)
        await telegram.initialize()  # ToDo: move async initialization to factories
        await telegram.set_webhook(webhook_url)

    async def on_shutdown():
        await service_provider.provide(TelegramService).shutdown()

    app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])
    app.include_router(telegram_webhook_router)
    app.service_provider = service_provider  # type: ignore
    return app


@service_factories.add
def build_tg_application(env: Env) -> tge.Application:
    return tge.Application.builder().token(env.telegram_api_token).build()


@service_factories.add
def build_tg_bot(application: tge.Application) -> Bot:
    return application.bot


@service_factories.add
def build_telegram_service(
    tg_application: tge.Application, service_provider: ServiceProvider
) -> TelegramService:
    return TelegramService(
        service_provider,
        tg_application,
        telegram_handlers,
    )


@service_factories.add
def build_mongo_storage(env: Env) -> MongoStorage:
    return MongoStorage.from_mongo_uri(env.mongo_uri)


@service_factories.add
def choose_storage_implementation(mongo_storage: MongoStorage) -> Storage:
    return mongo_storage


@service_factories.add
def build_webhook_full_url(env: Env) -> WebhookFullUrl:
    return url_join(env.bot_host, TELEGRAM_WEBHOOK_PATH)


@service_factories.add
def build_predictor(image_gen: ImageGenerator, assets: AssetsBox) -> Predictor:
    return Predictor(image_gen, assets)


@service_factories.add
def build_image_generator(assets: AssetsBox) -> ImageGenerator:
    return ImageGenerator(assets)


@service_factories.add
def build_assets_box() -> AssetsBox:
    return AssetsBox.load_assets()
