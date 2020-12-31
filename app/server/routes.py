from starlette.routing import Route, Request
from starlette.responses import Response, FileResponse

from app.config.dotenv import get_env
from app.bot.dispatcher import get_dispatcher

import img_gen

env = get_env()
dispatcher = get_dispatcher()


def check_run(request: Request):
    return Response("Server is running")


async def telegram_webhook(request: Request):
    print("GET REQ")
    dispatcher.process_update(await request.json())
    print("END REQ")
    return Response("Ok")


routes = [
    Route(env.telegram.webhook_route, telegram_webhook, methods=["POST"]),
    Route('/', check_run),
]
