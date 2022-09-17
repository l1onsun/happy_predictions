from typing import Optional, Protocol, runtime_checkable

from happy_predictions.services.storage.models import DatabaseUser


@runtime_checkable
class Storage(Protocol):
    async def find_user(self, user_id: int) -> Optional[DatabaseUser]:
        ...

    async def new_user(
        self, user_id: int, prediction_id: int, prediction_background: str
    ) -> None:
        ...
