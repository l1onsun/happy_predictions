from app.config.dotenv import get_env

from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@lru_cache
def get_db_client() -> AsyncIOMotorClient:
    env = get_env()
    connect_uri = "mongodb://{}:{}@{}:{}".format(env.mongo.user, env.mongo.password, env.mongo.host, env.mongo.port)
    if env.mongo.auth_db is not None:
        connect_uri += "/{}".format(env.mongo.auth_db)
    return AsyncIOMotorClient(connect_uri,
                              maxPoolSize=env.mongo.max_connections,
                              minPoolSize=env.mongo.min_connections)


@lru_cache
def get_database() -> AsyncIOMotorDatabase:
    env = get_env()
    return get_db_client()[env.mongo.db]
