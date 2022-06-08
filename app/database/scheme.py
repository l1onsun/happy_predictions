from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal


# constants
class SchemeConfig:
    collection_user = "tg_user"
    collection_user_unique = "id"
    collection_user_prediction_idx = "prediction_idx"
    collection_user_prediction_background = "prediction_background"
    # employee_indexes = [(employee_company, 1), (employee_job_title, 1), (employee_name, 1)]


# class to validate data input to mongo
class DatabaseUser(BaseModel):
    id: int = Field(..., alias=SchemeConfig.collection_user_unique)
    prediction: int = Field(..., alias=SchemeConfig.collection_user_prediction_idx)
    background: str = Field(
        ..., alias=SchemeConfig.collection_user_prediction_background
    )
