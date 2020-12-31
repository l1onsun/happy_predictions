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

def gunicorn():
    subprocess.run(["gunicorn", "app.server.asgi:app",
                    "-k", "uvicorn.workers.UvicornWorker", "-c", "app/config/gunicorn.py"])

def deploy():
    for cmd in evn.fire_deploy.split():
        subprocess.run(["python", "-m", "app.script.fire", cmd])

if __name__ == '__main__':
    fire.Fire()