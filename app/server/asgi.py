from starlette.applications import Starlette

from app.const import PORT
from app.env import get_env
from app.server.routes import routes
from app.server.events import on_startup, on_shutdown

env = get_env()

app = Starlette(
    debug=env.debug, on_startup=on_startup, on_shutdown=on_shutdown, routes=routes
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
