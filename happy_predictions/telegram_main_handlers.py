import telegram as tg
import structlog as structlog

from happy_predictions.const import YEAR
from happy_predictions.predictor.predictor import Predictor
from happy_predictions.storage.models import DatabaseUser
from happy_predictions.storage.storage import Storage
from happy_predictions.telegram.fix_telegram_types import Update
from happy_predictions.telegram.provided_handlers import ProvidedHandlers

main_handlers = ProvidedHandlers()

log = structlog.get_logger()


def keyboard(*tables: dict[str, str]):
    inline_keyboard = [
        [
            tg.InlineKeyboardButton(text, callback_data=callback_data)
            for text, callback_data in table.items()
        ]
        for table in tables
    ]
    return tg.InlineKeyboardMarkup(inline_keyboard)


@main_handlers.add_start_handler
async def on_start(update: Update):
    if not update.effective_chat:
        raise RuntimeError("No effective chat")

    await update.effective_chat.send_photo(
        "https://cs10.pikabu.ru/post_img/big/2018/08/02/9/1533224874120297049.jpg"
    )
    await update.effective_chat.send_message(
        f"Мяу... Хочешь получить предсказание на {YEAR} год?",
        reply_markup=keyboard({"Получить предсказание от Котика!": "prediction"}),
    )


@main_handlers.add_callback_query_handler
async def make_prediction_callback(
    update: Update, storage: Storage, predictor: Predictor
):
    user: tg.User = update.callback_query.from_user  # type: ignore
    if not update.effective_chat:
        raise RuntimeError("No effective chat")

    found_user = await storage.find_user(user.id)
    if found_user is not None and found_user.prediction_2026:
        await update.effective_chat.send_message(
            f"Муррр... {user.name}, хочешь ещё одно предсказание? "
            f"К сожалению или к счастью, не получится 😾\n\n"
            f"Всем положено только одно предсказание на этот год 😽"
        )
        image = predictor.get_image(found_user.prediction_2026)
    elif found_user is None:
        await update.effective_chat.send_message(
            f"Привет {user.name}! Хочешь узнать что ждет тебя в {YEAR} году?\n\n"
            f"Моё предсказание:"
        )
        prediction_params = predictor.get_random_prediction_params()
        image = predictor.get_image(prediction_params)
        await storage.new_user(DatabaseUser.new(user, prediction_2026=prediction_params))
    elif found_user:
        await update.effective_chat.send_message(
            f"Привет {user.name}, мой старый друг! Сбылось моё предсказание на {YEAR-1}? Вот-вот!\n\n"
            f"А в этом {YEAR} году тебя ждёт Новое предсказание 🎄"
        )
        prediction_params = predictor.get_random_prediction_params()
        image = predictor.get_image(prediction_params)
        await storage.full_update_user(DatabaseUser.new(user, old_prediction=found_user.prediction, prediction_2026=prediction_params))
    else:
        await update.effective_chat.send_message(
            f"Произошла какая-то странная ошибка =( \n\nИзвините. Напишите админу",
        )
        return
        
    log.debug("before send photo")
    try:
        await update.effective_chat.send_photo(image)
    except:
        log.exception("Got error while sending photo")
        await update.effective_chat.send_message(
          f"Не получилось отправить предсказание 😿. Нажми ещё раз через минутку",
          reply_markup=keyboard({"Получить предсказание от Котика!": "prediction"}),
        )
        return
    log.debug("after send photo")
    await update.effective_chat.send_message(
        f"Ты получил свое мяу-предсказание на {YEAR} год?",
        reply_markup=keyboard({"Получить предсказание от Котика!": "prediction"}),
    )
