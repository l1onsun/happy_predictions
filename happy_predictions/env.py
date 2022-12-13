from pydantic import BaseSettings


class Env(BaseSettings):
    mongo_uri: str
    tg_token_main: str
    tg_token_admin: str
    bot_host: str  # https://ip_or_domain
    debug: bool
