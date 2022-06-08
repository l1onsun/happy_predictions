from app.database.get import get_database
from app.database.scheme import SchemeConfig, DatabaseUser
from typing import Optional


async def find_user(user_unique) -> Optional[DatabaseUser]:
    users = get_database()[SchemeConfig.collection_user]
    user: Optional[dict] = await users.find_one(
        {SchemeConfig.collection_user_unique: user_unique}
    )

    if user is None:
        return None
    return DatabaseUser(**user)


async def new_user(user_unique, prediction_index, prediction_background):
    users = get_database()[SchemeConfig.collection_user]
    user = DatabaseUser(
        **{
            SchemeConfig.collection_user_unique: user_unique,
            SchemeConfig.collection_user_prediction_idx: prediction_index,
            SchemeConfig.collection_user_prediction_background: prediction_background,
        }
    )
    await users.insert_one(user.dict(by_alias=True))
