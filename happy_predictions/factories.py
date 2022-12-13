from typing import cast

import telegram.ext as tge
from fastapi import FastAPI

from happy_predictions.admin_service import AdminService
from happy_predictions.const import (
    ADMIN_TELEGRAM_WEBHOOK_PATH,
    MAIN_TELEGRAM_WEBHOOK_PATH,
)
from happy_predictions.env import Env
from happy_predictions.factory_types import (
    AdminFullUrl,
    AdminTelegramService,
    MainFullUrl,
    MainTelegramService,
)
from happy_predictions.predictor.assets_manager import AssetsBox
from happy_predictions.predictor.image_generation import ImageGenerator
from happy_predictions.predictor.predictor import Predictor
from happy_predictions.service_provider.service_factory import ServiceFactories
from happy_predictions.service_provider.service_provider import ServiceProvider
from happy_predictions.storage.mongo_storage.mongo_storage import MongoStorage
from happy_predictions.storage.storage import Storage
from happy_predictions.telegram.telegram_service import TelegramService
from happy_predictions.telegram_admin_handlers import admin_handlers
from happy_predictions.telegram_main_handlers import main_handlers
from happy_predictions.telegram_webhook import router as telegram_webhook_router
from happy_predictions.utils import url_join

service_factories = ServiceFactories()


@service_factories.add
def build_fastapi(
    service_provider: ServiceProvider,
    main_webhook_url: MainFullUrl,
    admin_webhook_url: AdminFullUrl,
) -> FastAPI:
    async def on_startup():
        service_provider.solve_all()
        # ToDo: move async initialization to factories
        await service_provider.provide(MainTelegramService).initialize(main_webhook_url)
        await service_provider.provide(AdminTelegramService).initialize(
            admin_webhook_url
        )

    async def on_shutdown():
        await service_provider.provide(TelegramService).shutdown()

    app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])
    app.include_router(telegram_webhook_router)
    app.service_provider = service_provider  # type: ignore
    return app


@service_factories.add
def build_main_telegram_service(
    env: Env, service_provider: ServiceProvider
) -> MainTelegramService:
    return cast(
        MainTelegramService,
        TelegramService(
            service_provider,
            tge.Application.builder().token(env.tg_token_main).build(),
            main_handlers,
        ),
    )


@service_factories.add
def build_admin_telegram_service(
    env: Env, service_provider: ServiceProvider
) -> AdminTelegramService:
    return cast(
        AdminTelegramService,
        TelegramService(
            service_provider,
            tge.Application.builder().token(env.tg_token_admin).build(),
            admin_handlers,
        ),
    )


@service_factories.add
def build_mongo_storage(env: Env) -> MongoStorage:
    return MongoStorage.from_mongo_uri(env.mongo_uri)


@service_factories.add
def choose_storage_implementation(mongo_storage: MongoStorage) -> Storage:
    return mongo_storage


@service_factories.add
def build_main_full_url(env: Env) -> MainFullUrl:
    return url_join(env.bot_host, MAIN_TELEGRAM_WEBHOOK_PATH)


@service_factories.add
def build_admin_full_url(env: Env) -> AdminFullUrl:
    return url_join(env.bot_host, ADMIN_TELEGRAM_WEBHOOK_PATH)


@service_factories.add
def build_predictor(image_gen: ImageGenerator, assets: AssetsBox) -> Predictor:
    return Predictor(image_gen, assets)


@service_factories.add
def build_image_generator(assets: AssetsBox) -> ImageGenerator:
    return ImageGenerator(assets)


@service_factories.add
def build_assets_box() -> AssetsBox:
    return AssetsBox.load_assets()


@service_factories.add
def build_admin_service() -> AdminService:
    return AdminService()
