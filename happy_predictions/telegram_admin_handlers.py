import structlog

from happy_predictions.admin_service import AdminService
from happy_predictions.predictor.assets_manager import (
    AssetsBox,
    MissingAsset,
    convert_at_sign,
)
from happy_predictions.predictor.image_generation import PredictionParams
from happy_predictions.predictor.predictor import Predictor
from happy_predictions.storage.models import DatabaseUser
from happy_predictions.storage.storage import Storage
from happy_predictions.telegram.fix_telegram_types import Update
from happy_predictions.telegram.provided_handlers import ProvidedHandlers
from happy_predictions.telegram_main_handlers import keyboard
from happy_predictions.utils import TimeCounter

log = structlog.get_logger()
admin_handlers = ProvidedHandlers()


@admin_handlers.add_start_handler
async def on_start(update: Update, storage: Storage, predictor: Predictor):
    if not (user := update.effective_user) or not update.effective_chat:
        log.warning(
            f"got message without effective_chat or effective_user {update.update_id=}"
        )
        return

    if not await storage.find_user(user.id):
        await storage.new_user(
            DatabaseUser.new(user, predictor.get_random_prediction_params())
        )

    await update.effective_chat.send_photo(
        "https://kartinki-dlya-srisovki.ru/wp-content"
        "/uploads/2019/05/kartinki-kot-pushin-1.png"
    )
    await update.effective_chat.send_message(
        "Мяу... Это админский канал, для проверки генерации картинок!\n"
        "Чтобы проверить предсказание, напиши в чат его номер или текст",
        reply_markup=keyboard(
            {"Или сначала выбери фон": "list_backgrounds"},
        ),
    )


@admin_handlers.add_callback_query_handler
async def make_prediction_callback(
    update: Update, assets: AssetsBox, admin_service: AdminService
):
    match update.callback_query.data:
        case "list_backgrounds":
            await update.effective_chat.send_message(
                "Выбери фон:",
                reply_markup=keyboard(
                    *[
                        {backround: backround}
                        for backround in assets.list_available_backgrounds()
                    ]
                ),
            )
        case background:
            await admin_service.choose_background(update.effective_user.id, background)
            max_text_id = len(assets.list_available_text_ids()) - 1
            await update.effective_chat.send_message(
                f"Выбран фон: {background}\n"
                "Теперь напиши номер или текст предсказания"
                f"(доступные номера: от 0 до {max_text_id})"
            )


@admin_handlers.add_message_handler
async def generate_prediction(
    update: Update, predictor: Predictor, admin_service: AdminService
):
    if not (update.effective_chat or update.effective_user):
        log.warning(
            f"got message without effective_chat or effective_user {update.update_id=}"
        )
        return
    if not (message := update.message or update.edited_message):
        log.warning(f"got message without message {update.update_id=}")
        return

    background = (
        await admin_service.get_selected_background(update.effective_user.id)
        or predictor.assets.list_available_backgrounds()[0]
    )

    try:
        text_id = int(message.text)
        with TimeCounter.start() as time_counter:
            image = predictor.get_image(PredictionParams(text_id, background))
    except (ValueError, MissingAsset):
        with TimeCounter.start() as time_counter:
            image = predictor.gen_custom_image(
                background, convert_at_sign(message.text)
            )

    await update.effective_chat.send_photo(image)
    await update.effective_chat.send_message(
        f"image generation time: {time_counter.milliseconds_passed()} ms",
        reply_markup=keyboard({"Сменить фон": "list_backgrounds"}),
    )
