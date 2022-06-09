import subprocess

import dotenv
import fire
import telegram

dotenv.load_dotenv(dotenv_path=".env")

from app.const import WEBHOOK_ROUTE, PORT
from app.env import Env

evn = Env()
bot = telegram.Bot(token=evn.telegram_api_token)


def set_webhook():
    return bot.set_webhook(url=f"{evn.bot_host}:{PORT}{WEBHOOK_ROUTE}")


def webhook_info():
    return bot.get_webhook_info()


def uvicorn():
    subprocess.run(["uvicorn", "--reload", "app.server.asgi:app", "--host", "0.0.0.0", "--port", f"{PORT}"])


def gunicorn():
    subprocess.run(
        [
            "gunicorn",
            "app.server.asgi:app",
            "-k",
            "uvicorn.workers.UvicornWorker",
            "-c",
            "app/config/gunicorn.py",
        ]
    )


def deploy():
    for cmd in evn.fire_deploy.split():
        subprocess.run(["python", "-m", "app.script.fire", cmd])


if __name__ == "__main__":
    fire.Fire()
