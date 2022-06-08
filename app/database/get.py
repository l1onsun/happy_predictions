from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.env import get_env


@lru_cache
def get_db_client() -> AsyncIOMotorClient:
    env = get_env()
    return AsyncIOMotorClient(
        env.mongo_uri,
    )


@lru_cache
def get_database() -> AsyncIOMotorDatabase:
    return get_db_client().get_default_database()
