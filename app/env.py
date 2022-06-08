from functools import lru_cache

from pydantic import BaseSettings


class Env(BaseSettings):
    mongo_uri: str
    telegram_api_token: str
    bot_host: str  # ip or domain
    secret: str  # just any random string
    debug: bool


@lru_cache
def get_env():
    return Env()
