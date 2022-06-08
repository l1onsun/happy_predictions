import asyncio
import time
from functools import lru_cache
from queue import Queue
from typing import Any

import telegram
from devtools import debug
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
)

from app.config import predictions
from app.const import YEAR
from app.database import crud
from app.database.scheme import DatabaseUser
from app.env import get_env


def error_handler(update, context: CallbackContext):
    debug("error handler:", update, context)


def keyboard(text):
    inline_keyboard = [
        [telegram.InlineKeyboardButton(text, callback_data="prediction")],
        # [
        #     telegram.InlineKeyboardButton("Настроить", callback_data="settings"),
        #     telegram.InlineKeyboardButton("Инфо", callback_data="info"),
        # ],
    ]
    return telegram.InlineKeyboardMarkup(inline_keyboard)


def command_start(update: telegram.Update, context: CallbackContext):
    if not update.effective_chat:
        raise RuntimeError("No effective chat")

    update.effective_chat.send_photo(
        "https://cs10.pikabu.ru/post_img/big/2018/08/02/9/1533224874120297049.jpg"
    )
    update.effective_chat.send_message(
        f"Мяу... Хочешь получить предсказание на {YEAR} год?",
        reply_markup=keyboard("Получить предсказание!"),
    )

    # time.sleep(4)
    # update.effective_chat.send_message("А что вы задумались? Ожидали увидеть здесь Белого Металлического Быка??")

    # update.message.reply_photo("https://cs10.pikabu.ru/post_img/big/2018/08/02/9/1533224874120297049.jpg")
    # update.message.reply_text(
    #     f"Мяу. Хочешь получить предсказание на {YEAR} год? "
    #     "(да, вы ожидали увидеть сдесь КРАСНОГО БЫКА, но ничего не поделать)",
    #     reply_markup=reply_markup
    # )


async def asycn_prediction_callback(update: telegram.Update, context: CallbackContext):
    user: telegram.User = update.callback_query.from_user  # type: ignore
    if not update.effective_chat:
        raise RuntimeError("No effective chat")

    found_user = await crud.find_user(user.id)
    if found_user is not None:
        update.effective_chat.send_message(
            f"{user.name}, хочешь ешё одно предсказание? К сожалению или к счастью, не получится )\n\n"
            f"Всем положено только одно предсказание на этот год!"
        )
        img = predictions.get_prediction(found_user.prediction, found_user.background)
    else:
        update.effective_chat.send_message(
            f"Привет {user.name}! Хочешь узнать что ждет тебя в {YEAR} году?\n\nМоё предсказание:"
        )
        index, background, img = predictions.get_random_prediction()
        await crud.new_user(user.id, index, background)
    update.effective_chat.send_photo(img)
    update.effective_chat.send_message(
        f"Кто ещё не получил своё предсказание на {YEAR} год?",
        reply_markup=keyboard("Получить предсказание!"),
    )


def prediction_callback(update: telegram.Update, context: CallbackContext):
    print("before create", time.time())
    asyncio.create_task(asycn_prediction_callback(update, context))
    print("after create", time.time())


class DispatcherWrapper:
    def __init__(self):
        env = get_env()
        self.bot = telegram.Bot(token=env.telegram_api_token)
        self._dispathcer = Dispatcher(
            bot=self.bot,
            update_queue=Queue(),
            workers=0,
        )
        self._command_handlers()
        self._callback_handlers()
        self._error_handlers()

    def _command_handlers(self):
        self._dispathcer.add_handler(CommandHandler("start", command_start))

    def _callback_handlers(self):
        self._dispathcer.add_handler(CallbackQueryHandler(prediction_callback))

    def _error_handlers(self):
        if not get_env().debug:
            self._dispathcer.add_error_handler(callback=error_handler)

    def process_update(self, update: dict[str, Any]):
        update_ = telegram.Update.de_json(update, self.bot)
        if not update_:
            raise RuntimeError("telegram.Update.de_json return None")
        return self._dispathcer.process_update(update_)


@lru_cache
def get_dispatcher():
    return DispatcherWrapper()
