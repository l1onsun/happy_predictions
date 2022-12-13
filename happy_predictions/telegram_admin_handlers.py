import time

import structlog

from happy_predictions.admin_service import AdminService
from happy_predictions.predictor.assets_manager import AssetsBox, MissingAsset
from happy_predictions.predictor.image_generation import PredictionParams
from happy_predictions.predictor.predictor import Predictor
from happy_predictions.telegram.fix_telegram_types import Update
from happy_predictions.telegram.provided_handlers import ProvidedHandlers
from happy_predictions.telegram_main_handlers import keyboard

log = structlog.get_logger()
admin_handlers = ProvidedHandlers()


@admin_handlers.add_start_handler
async def on_start(update: Update):
    if not update.effective_chat:
        raise RuntimeError("No effective chat")

    await update.effective_chat.send_photo(
        "https://kartinki-dlya-srisovki.ru/wp-content"
        "/uploads/2019/05/kartinki-kot-pushin-1.png"
    )
    await update.effective_chat.send_message(
        "Мяу... Это админский канал, для проверки генерации картинок!",
        reply_markup=keyboard(
            {"Как сгенерить предсказание?": "how_to"},
            {"Выбор background-а": "list_backgrounds"},
        ),
    )


@admin_handlers.add_callback_query_handler
async def make_prediction_callback(update: Update, assets: AssetsBox):
    match update.callback_query.data:
        case "how_to":
            await update.effective_chat.send_message(
                "Напиши через пробел backround и номер текста\nПример: b1.jpg 0\n",
                reply_markup=keyboard(
                    {"Или сначала выбери background": "list_backgrounds"}
                ),
            )
        case "list_backgrounds":
            await update.effective_chat.send_message(
                "Выбери background:",
                reply_markup=keyboard(
                    *[
                        {backround: backround}
                        for backround in assets.list_available_backgrounds()
                    ]
                ),
            )
        case background:
            await update.effective_chat.send_message(
                f"Выбран background: {background}\n"
                "Теперь напиши в чат номер предсказания\n",
                f"От 0 до {len(assets.list_available_text_ids()) - 1}",
            )


def parse_prediction_params(
    text: str, selected_background: str | None
) -> tuple[PredictionParams | None, str | None]:
    split = text.split(" ")

    error = None, (
        "Неправильный формат. Пример: b1.jpg 0"
        if selected_background is None
        else "Неправильный формат. Введи номер предсказания"
    )

    if len(split) == 1 and selected_background is not None:
        prediction_id_str = split[0]
    elif len(split) == 2:
        selected_background, prediction_id_str = split
    else:
        return error

    try:
        prediction_id = int(prediction_id_str)
    except ValueError:
        return error

    return PredictionParams(prediction_id, selected_background), None


@admin_handlers.add_message_handler
async def generate_prediction(
    update: Update, predictor: Predictor, admin_service: AdminService
):
    if not (update.effective_chat or update.effective_user):
        log.warning(f"got message without effective_chat {update.update_id=}")
        return
    if not (message := update.message or update.edited_message):
        log.warning(f"got message without message {update.update_id=}")
        return

    prediction_params, error = parse_prediction_params(
        message.text, admin_service.get_selected_background(update.effective_user.id)
    )
    if not prediction_params:
        await update.effective_chat.send_message(error)
        return

    try:
        start = time.time()
        image = predictor.get_prediction(prediction_params)
        end = time.time()
    except MissingAsset as e:
        await update.effective_chat.send_message(f"Не найдено предсказание\n{e}")
        return
    await update.effective_chat.send_photo(image)
    await update.effective_chat.send_message(
        f"image generation time: {end - start} sec"
    )
