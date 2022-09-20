import structlog as structlog
from fastapi import APIRouter, Depends, Request

from happy_predictions.const import TELEGRAM_WEBHOOK_PATH
from happy_predictions.provide_depends import provide
from happy_predictions.telegram.fix_telegram_types import Update
from happy_predictions.telegram.telegram_service import TelegramService

router = APIRouter()

log = structlog.get_logger()


async def parse_update(
    request: Request,
    telegram_service=provide(TelegramService),
) -> Update:
    request_json = await request.json()
    log.debug("update received", json=request_json)
    return telegram_service.parse_update_from_json(request_json)


@router.post(TELEGRAM_WEBHOOK_PATH)
async def webhook(
    update: Update = Depends(parse_update),
    telegram_service=provide(TelegramService),
):
    await telegram_service.process_update(update)


@router.get("/healthcheck")
async def healthcheck():
    log.debug("healthcheck")
    return "ok"