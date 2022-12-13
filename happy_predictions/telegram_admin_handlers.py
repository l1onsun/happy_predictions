# import telegram as tg
#
# from happy_predictions.const import YEAR
# from happy_predictions.predictor.predictor import Predictor
# from happy_predictions.storage.storage import Storage
from happy_predictions.telegram.fix_telegram_types import Update
from happy_predictions.telegram.provided_handlers import ProvidedHandlers
from happy_predictions.telegram_main_handlers import keyboard

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
        reply_markup=keyboard("Сгенерить предсказание!"),
    )


@admin_handlers.add_callback_query_handler
async def make_prediction_callback(update: Update):
    str_data = str(update.callback_query.data)
    await update.callback_query.answer(text=f"answer: {str_data}")
