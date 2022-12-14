from typing import Optional, Protocol, runtime_checkable

from happy_predictions.storage.models import DatabaseUser


@runtime_checkable
class Storage(Protocol):
    async def find_user(self, user_id: int) -> Optional[DatabaseUser]:
        ...

    async def new_user(self, user: DatabaseUser) -> None:
        ...

    async def admin_select_background(self, admin_id: int, background: str):
        ...
