import structlog

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
            {"Список background-ов": "list_backgrounds"},
        ),
    )


@admin_handlers.add_callback_query_handler
async def make_prediction_callback(update: Update, assets: AssetsBox):
    match update.callback_query.data:
        case "how_to":
            await update.effective_chat.send_message(
                "Напиши через пробел название backround и номер предсказания\n"
                "Пример: b1.jpg 0\n",
                reply_markup=keyboard({"Список background-ов": "list_backgrounds"}),
            )
        case "list_backgrounds":
            await update.effective_chat.send_message(
                "\n".join(assets.list_available_backgrounds()),
                reply_markup=keyboard({"Как сгенерить предсказание?": "how_to"}),
            )


@admin_handlers.add_message_handler
async def generate_prediction(update: Update, predictor: Predictor):
    if not update.effective_chat:
        log.warning(f"got message without effective_chat {update.update_id=}")
        return
    if not update.message:
        log.warning(f"got message without message {update.update_id=}")
        return
    try:
        background_name, prediction_id_str = update.message.text.split(" ")
        prediction_id = int(prediction_id_str)
    except ValueError:
        await update.effective_chat.send_message(
            "Неправильный формат. Пример: b1.jpg 0"
        )
        return
    try:
        image = predictor.get_prediction(
            PredictionParams(prediction_id, background_name)
        )
    except MissingAsset as e:
        await update.effective_chat.send_message(f"Не найдено предсказание\n{e}")
        return
    await update.effective_chat.send_photo(image)
