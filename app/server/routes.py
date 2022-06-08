from starlette.routing import Route, Request
from starlette.responses import Response

from app.bot.dispatcher import get_dispatcher
from app.const import WEBHOOK_ROUTE

dispatcher = get_dispatcher()


def check_run(request: Request):
    return Response("Server is running")


async def telegram_webhook(request: Request):
    print("GET REQ")
    dispatcher.process_update(await request.json())
    print("END REQ")
    return Response("Ok")


routes = [
    Route(WEBHOOK_ROUTE, telegram_webhook, methods=["POST"]),
    Route("/", check_run),
]
