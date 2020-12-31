from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request

from app.config.dotenv import get_env
from app.server.routes import routes
from app.server.events import on_startup, on_shutdown

env = get_env()

app = Starlette(
    debug=env.debug,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    routes=routes
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=env.gunicorn.host, port=env.gunicorn.port)