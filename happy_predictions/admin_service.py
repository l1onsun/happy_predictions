from dataclasses import dataclass, field


@dataclass
class AdminService:
    selected_background_admin_id: dict[int, str] = field(default_factory=dict)

    def get_selected_background(self, admin_user_id: int) -> str | None:
        return self.selected_background_admin_id.get(admin_user_id)
