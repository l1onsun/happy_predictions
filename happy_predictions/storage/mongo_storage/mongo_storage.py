# ToDo: Legacy code - needs refactoring

from dataclasses import dataclass
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from happy_predictions.storage.models import DatabaseUser
from happy_predictions.storage.storage import Storage


@dataclass
class MongoStorage(Storage):
    db: AsyncIOMotorDatabase

    def _user_coll(self):
        return self.db["user"]

    @classmethod
    def from_mongo_uri(cls, mongo_uri: str):
        return cls(AsyncIOMotorClient(mongo_uri).get_default_database())

    async def find_user(self, user_id: int) -> Optional[DatabaseUser]:
        user: dict | None = await self._user_coll().find_one({"_id": user_id})

        return DatabaseUser(**user) if user is not None else None

    async def new_user(self, user: DatabaseUser) -> None:
        await self._user_coll().insert_one(user.to_bson())

    async def full_update_user(self, user: DatabaseUser) -> None:
        await self._user_coll().update_one(
            {"_id": user.mongo_id},
            {"$set": user.to_bson()},
        )

    # TODO:
    # async def new_user(self, user: DatabaseUser) -> None:
    # user_data = user.to_bson()
    # await self._user_coll().update_one(
    #     {"_id": user.id},
    #     {"$set": user_data},  # Обновляем только переданные поля
    #     upsert=True
    # )

    async def admin_select_background(self, admin_id: int, background: str):
        await self._user_coll().update_one(
            {"_id": admin_id}, {"$set": {"admin_selected_background": background}}
        )
