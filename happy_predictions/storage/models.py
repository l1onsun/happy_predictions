from dataclasses import dataclass

import telegram as tg
from pydantic import BaseModel

from happy_predictions.predictor.image_generation import PredictionParams


@dataclass
class TelegramUser:
    is_bot: bool
    can_read_all_group_messages: bool | None
    username: str | None
    first_name: str
    last_name: str | None
    can_join_groups: bool | None
    supports_inline_queries: bool | None
    id: int
    language_code: str | None
    is_premium: bool | None
    added_to_attachment_menu: bool | None

    @classmethod
    def from_tg_user(cls, user: tg.User):
        return cls(**user.to_dict())


class DatabaseUser(BaseModel):
    _id: int
    prediction: PredictionParams
    telegram_user: TelegramUser
    admin_selected_background: str | None

    @classmethod
    def new(cls, tg_user: tg.User, prediction_params: PredictionParams):
        return cls(
            _id=tg_user.id,
            prediction=prediction_params,
            telegram_user=TelegramUser.from_tg_user(tg_user),
            admin_selected_background=None,
        )
