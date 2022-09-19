from dataclasses import dataclass

from PIL import Image

from happy_predictions.predictor.assets_manager import AssetsBox
from happy_predictions.predictor.image_generation import (
    ImageGenerator,
    PredictionParams,
)


@dataclass
class Predictor:
    image_gen: ImageGenerator
    assets: AssetsBox

    def get_prediction(self, params: PredictionParams) -> Image:
        return self.image_gen.gen_image_cached(params)

    def get_random_prediction_params(self) -> PredictionParams:
        return PredictionParams(
            text_id=self.assets.random_prediction_text_id(),
            background_name=self.assets.random_background_name(),
        )
