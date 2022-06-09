from app.env import get_env

env = get_env()
WEBHOOK_ROUTE = f"/{env.secret}/tg_web_hook"
PORT = 8080
YEAR = 2022
