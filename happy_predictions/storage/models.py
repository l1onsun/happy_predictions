from dataclasses import asdict, dataclass

import telegram as tg
from pydantic import BaseModel, Field

from happy_predictions.predictor.image_generation import PredictionParams
from happy_predictions.utils import JsonType


@dataclass
class TelegramUser:
    is_bot: bool
    first_name: str
    id: int
    can_read_all_group_messages: bool | None = None
    username: str | None = None
    last_name: str | None = None
    can_join_groups: bool | None = None
    supports_inline_queries: bool | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None

    @classmethod
    def from_tg_user(cls, user: tg.User):
        return cls(**user.to_dict())


class DatabaseUser(BaseModel):
    mongo_id: int = Field(..., alias="_id")
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

    def to_bson(self) -> JsonType:
        return self.dict(by_alias=True, exclude={"telegram_user", "prediction"}) | {
            "telegram_user": asdict(self.telegram_user),
            "prediction": asdict(self.prediction),
        }
