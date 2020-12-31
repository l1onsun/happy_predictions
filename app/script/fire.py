import fire
import telegram
import subprocess

from app.config.dotenv import get_env

evn = get_env()
bot = telegram.Bot(token=evn.telegram.token)

def set_webhook():
    return bot.set_webhook(url=f"{evn.telegram.bot_host}{evn.telegram.webhook_route}")

def webhook_info():
    return bot.get_webhook_info()

def uvicorn():
    subprocess.run(["uvicorn", "--reload", "app.server.asgi:app", "--port", "8080"])

def deploy():
    subprocess.run(["python", "-m", __file__, evn.fire_deploy])

if __name__ == '__main__':
    fire.Fire()