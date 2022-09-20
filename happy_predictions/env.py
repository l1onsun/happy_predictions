from pydantic import BaseSettings


class Env(BaseSettings):
    mongo_uri: str
    telegram_api_token: str
    bot_host: str  # https://ip_or_domain
    debug: bool
