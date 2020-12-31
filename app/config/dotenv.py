from functools import lru_cache

from pydantic import BaseSettings
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

@lru_cache
def get_env():
    return EnvSettings()


# def get_mongo_env():
#     return get_env().mongo
#
# def get_gunicorn_env():
#     return get_env().gunicorn
#
# def get_telegram_env():
#     return get_env().bot

class AppSettings(BaseSettings):
    host: Optional[str] = "localhost"
    port: Optional[str] = "8080"

class MongoSettings(BaseSettings):
    db: str
    user: str
    auth_db: Optional[str] = None
    password: str
    host: str
    port: int
    min_connections: int
    max_connections: int

    full_uri: Optional[str] = None

    class Config:
        env_prefix = "MONGO_"


class GunicornSettings(BaseSettings):
    workers_per_core: Optional[int] = 1
    max_workers: Optional[int] = 2
    web_concurrency: Optional[int] = None
    host: Optional[str] = "localhost"
    port: Optional[str] = "8080"
    timeout: Optional[int] = 120
    keepalive: Optional[int] = 5

    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    ssl_chain: Optional[str] = None

    class Config:
        env_prefix = "GUNICORN_"


class TelegramSettings(BaseSettings):
    token: str
    bot_host: str
    webhook_route: str
    bot_name: str
    thread_workers: str

    class Config:
        env_prefix = "TELEGRAM_"


class EnvSettings(BaseSettings):
    debug: bool = False
    fire_deploy: str
    mongo = MongoSettings()
    gunicorn = GunicornSettings()
    telegram = TelegramSettings()
