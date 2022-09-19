from pydantic import BaseModel, Field

from happy_predictions.predictor.image_generation import PredictionParams


class SchemeConfig:
    user = "tg_user"
    user_unique = "id"
    user_prediction_idx = "prediction_idx"
    user_prediction_background = "prediction_background"


class DatabaseUser(BaseModel):
    id: int = Field(..., alias=SchemeConfig.user_unique)
    prediction: int = Field(..., alias=SchemeConfig.user_prediction_idx)
    background: str = Field(..., alias=SchemeConfig.user_prediction_background)

    def prediction_params(self) -> PredictionParams:
        return PredictionParams(self.prediction, self.background)
