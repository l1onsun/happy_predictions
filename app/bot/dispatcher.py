import telegram
from telegram.ext import Dispatcher, CommandHandler, CallbackContext, CallbackQueryHandler, Handler
from functools import lru_cache
from app.config.dotenv import get_env
from app.config import predictions

from app.database.scheme import DatabaseUser
from app.database import crud
import asyncio

from typing import Any
import time
from devtools import debug


def error_handler(update, context: CallbackContext):
    debug("error handler:", update, context)

def keyboard(text):
    keyboard = [
        [telegram.InlineKeyboardButton(text, callback_data='prediction')],
        # [
        #     telegram.InlineKeyboardButton("Настроить", callback_data='settings'),
        #     telegram.InlineKeyboardButton("Инфо", callback_data='info')]
    ]
    return telegram.InlineKeyboardMarkup(keyboard)

def command_start(update: telegram.Update, context: CallbackContext):

    update.effective_chat.send_photo("https://cs10.pikabu.ru/post_img/big/2018/08/02/9/1533224874120297049.jpg")
    update.effective_chat.send_message("Мяу... Хочешь получить предсказание на 2021 год?",
                                       reply_markup=keyboard("Получить предсказание!"))

    # time.sleep(4)
    # update.effective_chat.send_message("А что вы задумались? Ожидали увидеть здесь Белого Металлического Быка??")

    # update.message.reply_photo("https://cs10.pikabu.ru/post_img/big/2018/08/02/9/1533224874120297049.jpg")
    # update.message.reply_text("Мяу. Хочешь получить предсказание на 2021 год? (да, вы ожидали увидеть сдесь КРАСНОГО БЫКА, но ничего не поделать)", reply_markup=reply_markup)


async def asycn_prediction_callback(update: telegram.Update, context: CallbackContext):
    print("async start")
    user: telegram.User = update.callback_query.from_user

    update.effective_chat.send_message(f"Предсказываю предсказание для {user.name}...")

    found_user = await crud.find_user(user.id)
    if found_user is not None:
        found_user: DatabaseUser
        img = predictions.get_prediction(found_user.prediction, found_user.background)
    else:
        index, background, img = predictions.get_random_prediction()
        await crud.new_user(user.id, index, background)
    update.effective_chat.send_photo(img, reply_markup=keyboard("Кто ещё хочет предсказание?"))
    print("async end")


def prediction_callback(update: telegram.Update, context: CallbackContext):
    import time
    print("before create", time.time())
    asyncio.create_task(asycn_prediction_callback(update, context))
    print("after create", time.time())


class DispatcherWrapper():
    def __init__(self):
        env = get_env()
        self.bot = telegram.Bot(token=env.telegram.token)
        self._dispathcer = Dispatcher(
            bot=self.bot,
            update_queue=None,
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
        update = telegram.Update.de_json(update, self.bot)
        return self._dispathcer.process_update(update)


@lru_cache
def get_dispatcher():
    return DispatcherWrapper()
