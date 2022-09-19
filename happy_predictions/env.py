from pydantic import BaseSettings


class Env(BaseSettings):
    mongo_uri: str
    telegram_api_token: str
    bot_host: str  # ip or domain
    debug: bool
