from typing import Type

import structlog as structlog
from fastapi import APIRouter, Depends, Request

from happy_predictions.const import (
    ADMIN_TELEGRAM_WEBHOOK_PATH,
    MAIN_TELEGRAM_WEBHOOK_PATH,
)
from happy_predictions.factory_types import AdminTelegramService, MainTelegramService
from happy_predictions.provide_depends import provide
from happy_predictions.telegram.fix_telegram_types import Update
from happy_predictions.telegram.telegram_service import TelegramService

router = APIRouter()

log = structlog.get_logger()


def parse_update(telegram_service_type: Type[TelegramService]) -> Update:
    async def parse_update_for_selected_service(
        request: Request,
        telegram_service=provide(telegram_service_type),
    ) -> Update:
        request_json = await request.json()
        log.debug("update received", json=request_json)
        return telegram_service.parse_update_from_json(request_json)

    return Depends(parse_update_for_selected_service)


@router.post(MAIN_TELEGRAM_WEBHOOK_PATH)
async def main_webhook(
    update=parse_update(MainTelegramService),
    telegram_service=provide(MainTelegramService),
):
    await telegram_service.process_update(update)


@router.post(ADMIN_TELEGRAM_WEBHOOK_PATH)
async def admin_webhook(
    update=parse_update(AdminTelegramService),
    telegram_service=provide(AdminTelegramService),
):
    await telegram_service.process_update(update)


@router.get("/healthcheck")
async def healthcheck():
    log.debug("healthcheck")
    return "ok"
