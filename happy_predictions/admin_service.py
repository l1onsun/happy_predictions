from dataclasses import dataclass

from happy_predictions.storage.storage import Storage


@dataclass
class AdminService:
    storage: Storage

    async def get_selected_background(self, admin_user_id: int) -> str | None:
        user = await self.storage.find_user(admin_user_id)
        return user.admin_selected_background if user else None

    async def choose_background(self, admin_id: int, background_name: str) -> None:
        await self.storage.admin_select_background(admin_id, background_name)
