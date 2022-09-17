from fastapi import APIRouter, Depends, Request

from happy_predictions.const import TELEGRAM_WEBHOOK_PATH
from happy_predictions.provide_depends import provide
from happy_predictions.services.telegram.telegram_service import TelegramService

router = APIRouter()


async def parse_update(
    request: Request,
    telegram_service=provide(TelegramService),
):
    return telegram_service.parse_update_from_json(await request.json())


@router.post(TELEGRAM_WEBHOOK_PATH)
async def webhook(
    update=Depends(parse_update),
    telegram_service=provide(TelegramService),
):
    await telegram_service.process_update(update)
