from dataclasses import dataclass
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from happy_predictions.services.storage.models import DatabaseUser, SchemeConfig
from happy_predictions.services.storage.storage import Storage


@dataclass
class MongoStorage:
    db: AsyncIOMotorDatabase

    @classmethod
    def from_mongo_uri(cls, mongo_uri: str):
        return cls(AsyncIOMotorClient(mongo_uri).get_default_database())

    async def find_user(self, user_id: int) -> Optional[DatabaseUser]:
        users = self.db[SchemeConfig.user]
        user: Optional[dict] = await users.find_one({SchemeConfig.user_unique: user_id})

        if user is None:
            return None
        return DatabaseUser(**user)

    async def new_user(
        self, user_id: int, prediction_id: int, prediction_background: str
    ) -> None:
        users = self.db[SchemeConfig.user]
        user = DatabaseUser(
            **{
                SchemeConfig.user_unique: user_id,
                SchemeConfig.user_prediction_idx: prediction_id,
                SchemeConfig.user_prediction_background: prediction_background,
            }
        )
        await users.insert_one(user.dict(by_alias=True))


assert issubclass(MongoStorage, Storage), "MongoStorage should implement Storage"
