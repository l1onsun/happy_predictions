import telegram as tg

from happy_predictions.const import YEAR
from happy_predictions.services.predictions import Predictions
from happy_predictions.services.storage.storage import Storage
from happy_predictions.services.telegram.fix_telegram_types import Update
from happy_predictions.services.telegram.provided_handlers import ProvidedHandlers

telegram_handlers = ProvidedHandlers()


def keyboard(text):
    inline_keyboard = [
        [tg.InlineKeyboardButton(text, callback_data="prediction")],
    ]
    return tg.InlineKeyboardMarkup(inline_keyboard)


@telegram_handlers.add_start_handler
async def on_start(update: Update):
    if not update.effective_chat:
        raise RuntimeError("No effective chat")

    await update.effective_chat.send_photo(
        "https://cs10.pikabu.ru/post_img/big/2018/08/02/9/1533224874120297049.jpg"
    )
    await update.effective_chat.send_message(
        f"Мяу... Хочешь получить предсказание на {YEAR} год?",
        reply_markup=keyboard("Получить предсказание!"),
    )


@telegram_handlers.add_callback_query_handler
async def make_prediction_callback(
    update: Update, storage: Storage, predictions: Predictions
):
    user: tg.User = update.callback_query.from_user  # type: ignore
    if not update.effective_chat:
        raise RuntimeError("No effective chat")

    found_user = await storage.find_user(user.id)
    if found_user is not None:
        await update.effective_chat.send_message(
            f"{user.name}, хочешь ешё одно предсказание? "
            f"К сожалению или к счастью, не получится )\n\n"
            f"Всем положено только одно предсказание на этот год!"
        )
        img = predictions.get_prediction(found_user.prediction, found_user.background)
    else:
        await update.effective_chat.send_message(
            f"Привет {user.name}! Хочешь узнать что ждет тебя в {YEAR} году?\n\n"
            f"Моё предсказание:"
        )
        index, background, img = predictions.get_random_prediction()
        await storage.new_user(user.id, index, background)
    await update.effective_chat.send_photo(img)
    await update.effective_chat.send_message(
        f"Кто ещё не получил своё предсказание на {YEAR} год?",
        reply_markup=keyboard("Получить предсказание!"),
    )
